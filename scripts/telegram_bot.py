from dialogue_system import UtteranceGenerator
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

class TelegramDialogueSystem:
    def __init__(
        self,
        check_point_path: str,
        dict_dir: str,
        spm_model_path: str,
        auth_key: str='',
        system_name: str='system',
        initial_message: str='はじめまして。お話しましょう。',
        memory_num: int=3,
        use_cuda: bool=False,
    ):
        self.system = UtteranceGenerator(
            check_point_path=check_point_path,
            use_cuda=use_cuda
        )
        self.system_name = system_name
        self.initial_message = initial_message
        self.memory_num = memory_num
        self.auth_key = auth_key

    def start(self, bot, update):
        user_input = {'utt': None, 'sessionId': str(update.message.from_user.id)}
        update.message.reply_text({"utt":self.initial_message, "end":False})

    def message(self, bot, update):
        user_input = {'utt': update.message.text.replace("！", "!").replace("？", "?").replace("．", "。").replace("，", "、"), 'sessionId': str(update.message.from_user.id)}
        if '/reset' in user_input["utt"]:
            self.system.context_list = []
            system_output = {"utt":self.initial_message, "end":False}
        else:
            system_output = self.system.reply(user_input)
        self.system.context_list.append('[SEP][SPK1]'+system_output["utt"])

        if len(self.system.context_list) > self.memory_num:
                del self.system.context_list[0]
                self.system.context_list[0] = self.system.context_list[0].replace("[SEP]", "")

        update.message.reply_text(system_output["utt"])

    def run(self):
        updater = Updater(self.auth_key)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(MessageHandler(Filters.text, self.message))
        updater.start_polling()
        updater.idle()