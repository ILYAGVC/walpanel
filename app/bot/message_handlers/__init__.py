from . import main_admin_message_handlers


def register_all_message_handlers(bot):
    main_admin_message_handlers.message_handlers(bot)
