from dialogue_system import UtteranceGenerator

class CLIDialogueSystem:
    def __init__(
        self,
        check_point_path: str,
        dict_dir: str,
        spm_model_path: str,
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

    def message(self, user_input):

        input_text = user_input.replace("！", "!").replace("？", "?").replace("．", "。").replace("，", "、")

        # replyメソッドによりシステム発話を生成
        system_output = self.system.reply(input_text)

        self.system.context_list.append('[SEP][SPK1]'+system_output)

        # システム発話を返す
        return self.system.context_list[-1]

    def run(self):
        print(self.system_name+':'+self.initial_message)
        self.system.context_list.append('[SPK1]'+self.initial_message)
        while True:
            user_input = input().rstrip("\n")

            if "/reset" in user_input:
                # リセットコマンドが入力された場合に対話履歴をリセット
                self.system.context_list = []
                print(self.system_name+':'+self.initial_message)
                continue

            system_output = self.message(user_input)
            if len(self.system.context_list) > self.memory_num:
                del self.system.context_list[0]
                self.system.context_list[0] = self.system.context_list[0].replace("[SEP]", "")
            print(self.system_name+':'+system_output)