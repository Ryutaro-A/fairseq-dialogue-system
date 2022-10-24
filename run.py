from .scripts.telegram_bot import TelegramDialogueSystem
from .scripts.cli_bot import CLIDialogueSystem


import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--mode', type=str, help='cli or telegram', choices=['cli', 'telegram'])
parser.add_argument('--check_point_path', type=str, help='check pointファイルのパス')
parser.add_argument('--dict_dir', type=str, help='fairseqで前処理したdictのディレクトリ')
parser.add_argument('--spm_model_path', type=str, help='学習済みsentencepieceのモデルパス')
parser.add_argument('--system_name', type=str, help='表示するシステムの名前(コマンドラインでの実行のみ)')
parser.add_argument('--initial_message', type=str, help='システムが最初に出力する発話(はじめまして，など)')
parser.add_argument('--memory_num', type=int, help='対話履歴をどこまで保存するか')
parser.add_argument('--check_point_path', type=str, help='check pointファイルのパス')
parser.add_argument('--use_cuda', action='store_true', help='cudaを使うか')

args = parser.parse_args()

with open('./authorize_key/key.txt', mode='r', encoding='utf-8') as f:
    auth_key = f.read().rstrip('\n')

if  args.mode == "telegram":
    if auth_key == "" or "sample key" in auth_key:
        print('Not found auth key.')
        exit(1)
    telegram_bot_system = TelegramDialogueSystem(
        check_point_path=args.check_point_path,
        dict_dir=args.dict_dir,
        spm_model_path=args.spm_model_path,
        auth_key=auth_key,
        system_name=args.system_name,
        initial_message=args.initial_message,
        memory_num=args.memory_num,
        use_cuda=args.use_cuda,
    )
    telegram_bot_system.run()
else:
    cli_bot_system = CLIDialogueSystem(
        check_point_path=args.check_point_path,
        dict_dir=args.dict_dir,
        spm_model_path=args.spm_model_path,
        system_name=args.system_name,
        initial_message=args.initial_message,
        memory_num=args.memory_num,
        use_cuda=args.use_cuda
    )
    cli_bot_system.run()

