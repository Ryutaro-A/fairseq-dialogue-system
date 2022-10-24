# fairseq-dialogue-system

これはFairseqを使ってSeq2seqモデルから簡単に非タスク志向型対話システムが構築出来るスクリプトです．

オリジナルのFairseqのコードを読み，拡張する形で開発しました．

GPUにも対応しており，FP16で推論が可能です．

## 使用方法

| コマンド         | 値                 | 説明                                                                       |
| ---------------- | ------------------ | -------------------------------------------------------------------------- |
| mode             | cli or telegram    | コマンドライン上かtelegramのどちらで対話システムを動作させるか決定します． |
| check_point_path | パス               | 対話システムに用いるモデルのパス．（お手軽なのはNTTの対話モデル）          |
| dict_dir         | パス               | Fairseqで前処理した際に出力される辞書データのあるディレクトリのパス．      |
| spm_model_path   | パス               | 学習済みのSentencepieceモデルのファイルパス．                              |
| system_name      | e.g. Siri          | コマンドライン上で表示されるシステムの名前(cli modeでのみ有効)             |
| initial_message  | e.g. こんにちは。 | システムが最初に出力するメッセージ．対話履歴にも含まれる．                 |
| memory_num       | int                | システムが記憶する対話履歴の最大発話数                                     |
| use_cuda         | -                  | このオプションつけることでGPUが有効になり，FP16で高速に推論される．        |

```
python run.py --mode cli \
    --check_point_path ./checkpoints/best_model.pt
    --dict_dir ./data/sample/
    --spm_model_path ./data/spk32.model
    --system_name Siri
    --initial_message こんにちは。初めまして。
    --memory_num 4
    --use_cuda
```


## ライセンス

このソフトウェアは、MITライセンスのもとで公開されています。LICENSE.txtをご覧ください。

## 連絡先

Twitter: [@ryu1104_m](https://twitter.com/ryu1104_m)

Mail: ryu1104.as[at]gmail.com
