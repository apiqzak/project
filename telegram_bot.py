import asyncio
import logging
import os
import tempfile
from pathlib import Path

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from test_pose import VALID_EXERCISES, analyze_image_file, format_report


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
LOGGER = logging.getLogger(__name__)


def exercise_keyboard():
    buttons = [
        [InlineKeyboardButton(exercise.title(), callback_data=f"exercise:{exercise}")]
        for exercise in VALID_EXERCISES
    ]
    return InlineKeyboardMarkup(buttons)


def parse_exercise(text):
    if not text:
        return None

    tokens = text.lower().replace("/", " ").split()
    for token in tokens:
        if token in VALID_EXERCISES:
            return token
    return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send a workout photo with a caption like 'squat', 'pushup', 'plank', or 'pullup'.\n"
        "You can also choose the exercise first using /exercise.",
        reply_markup=exercise_keyboard(),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/exercise - choose exercise type\n"
        "/set squat - save exercise type\n\n"
        "Then send a clear full-body photo. Captions also work, for example: pullup",
        reply_markup=exercise_keyboard(),
    )


async def exercise_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Choose the exercise to analyze:", reply_markup=exercise_keyboard())


async def set_exercise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    exercise = parse_exercise(" ".join(context.args))
    if exercise is None:
        await update.message.reply_text(
            "Please choose one of: squat, pushup, plank, pullup",
            reply_markup=exercise_keyboard(),
        )
        return

    context.user_data["exercise"] = exercise
    await update.message.reply_text(f"Exercise set to {exercise.upper()}. Now send a photo.")


async def exercise_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    exercise = query.data.split(":", 1)[1]
    context.user_data["exercise"] = exercise
    await query.edit_message_text(f"Exercise set to {exercise.upper()}. Now send a workout photo.")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption_exercise = parse_exercise(update.message.caption)
    exercise = caption_exercise or context.user_data.get("exercise")

    if exercise is None:
        await update.message.reply_text(
            "Which exercise is this? Choose one, or resend the photo with a caption like 'squat'.",
            reply_markup=exercise_keyboard(),
        )
        return

    status_message = await update.message.reply_text("Analyzing posture...")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        input_path = temp_path / "input.jpg"
        output_path = temp_path / "output.jpg"

        photo = update.message.photo[-1]
        telegram_file = await photo.get_file()
        await telegram_file.download_to_drive(str(input_path))

        try:
            report = await asyncio.to_thread(
                analyze_image_file,
                str(input_path),
                exercise,
                str(output_path),
                False,
            )
        except Exception as exc:
            LOGGER.exception("Pose analysis failed")
            await status_message.edit_text(f"Analysis failed: {exc}")
            return

        caption = (
            f"{report['exercise'].upper()} | {report['phase']}\n"
            f"Score: {report['score']}/{report['total']} checks passed"
        )
        with output_path.open("rb") as image_file:
            await update.message.reply_photo(photo=image_file, caption=caption)

        await update.message.reply_text(format_report(report))
        await status_message.delete()


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    exercise = parse_exercise(update.message.text)
    if exercise is None:
        await update.message.reply_text(
            "Send a workout photo, or choose an exercise first.",
            reply_markup=exercise_keyboard(),
        )
        return

    context.user_data["exercise"] = exercise
    await update.message.reply_text(f"Exercise set to {exercise.upper()}. Now send a photo.")


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("Set TELEGRAM_BOT_TOKEN before running the bot")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("exercise", exercise_command))
    app.add_handler(CommandHandler("set", set_exercise))
    app.add_handler(CallbackQueryHandler(exercise_button, pattern=r"^exercise:"))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    LOGGER.info("Workout posture bot is running")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
