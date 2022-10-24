import torch
from fairseq import checkpoint_utils, tasks
from omegaconf import OmegaConf
import fairseq
from fairseq.sequence_generator import SequenceGenerator
import sentencepiece as spm


class UtteranceGenerator:
    def __init__(
        self,
        dict_dir: str,
        spm_model_path: str,
        check_point_path: str,
        use_cuda: bool=False
    ):
        task_dic = {
            '_name': 'translation',
            'data': dict_dir,
            'source_lang': "src",
            'target_lang': "tgt",
            'train_subset': 'train',
            'dataset_impl': None,
            'required_seq_len_multiple': 1
        }
        task = tasks.setup_task(OmegaConf.create(task_dic))

        # 対話履歴のためのリスト
        self.context_list = []

        # checkpointのロード
        checkpoint = checkpoint_utils.load_checkpoint_to_cpu(check_point_path)

        # checkpointからモデル情報の抽出
        cfg = checkpoint["cfg"]
        model = task.build_model(cfg.model)

        # 学習済みのパラメータをロード
        model.load_state_dict(checkpoint["model"], strict=True, model_cfg=cfg.model)

        # タスクのロード
        task.load_state_dict(checkpoint["task_state"])

        # 辞書の読み込み
        self.src_dict = task.source_dictionary

        # CUDA or CPU
        if use_cuda:
            if torch.cuda.is_available():
                self.device = 'cuda'
                self.model = model.half().to(self.device)
            else:
                print('CUDA is not available on your device. So run CPU.')
                self.device = 'cpu'
                self.model = model.to(self.device)
        else:
            self.device = 'cpu'
            self.model = model.to(self.device)

        # Generatorの定義
        diverbeamsearch =  fairseq.search.DiverseBeamSearch(self.src_dict, num_groups=5, diversity_strength=0.5)
        self.generator = SequenceGenerator([self.model], self.src_dict, beam_size=80, min_len=10, no_repeat_ngram_size=3, search_strategy=diverbeamsearch)
        self.task = task

        # sentencepieceモデルのロード
        self.sp = spm.SentencePieceProcessor(model_file=spm_model_path)

    def decode_string(
        self,
        input_tensor: torch.Tensor
    ):
        s = self.src_dict.string(input_tensor)
        s = s.split()
        s = self.sp.decode_pieces(s)
        s = s.replace("<pad>", "")
        return s

    def reply(
        self,
        user_input: str
    ):
        user_input = '[SEP][SPK2]'+user_input
        self.context_list.append(user_input)
        src_token = self.src_dict.encode_line(" ".join(self.context_list), add_if_not_exist=False).unsqueeze(0)
        src_token_length = src_token.size()

        # inputデータ形式の定義
        data_dic = {
            'net_input': {
                'src_tokens': src_token.to(self.device),
                'src_lengths': src_token_length,
            },
        }

        # システム発話の推論
        translations = self.task.inference_step(self.generator, [self.model], data_dic)
        print(translations[0][0])
        for _, t in enumerate(translations):
            for i in range(20):
                generated = self.decode_string(t[i]["tokens"])
                return generated.replace("[BR]", "\n").replace("?", "？").replace("!", "！")