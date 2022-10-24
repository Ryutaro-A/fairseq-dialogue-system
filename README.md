# fairseq-dialogue-system

This is a script that allows you to easily build a non-task oriented interactive system from a Seq2seq model using Fairseq.

We have read and extended the original Fairseq code.

It is GPU-compatible and can be run on FP16.

## Usage

| Command          | Value           | Description                                                                              |
| ---------------- | --------------- | ---------------------------------------------------------------------------------------- |
| mode             | cli or telegram | This determines whether the dialog system will run on the command line or in a telegram. |
| check_point_path | path            | Path of the model to be used for the dialog system.                                      |
| dict_dir         | path            | The path of the directory containing the dictionary data to be preprocessed.             |
| spm_model_path   | path            | The file path of the trained Sentencepiece model.                                        |
| system_name      | e.g. Siri       | The name of the system as it appears on the command line (valid only in cli mode)        |
| initial_message  | e.g. Hello     | The first message output by the system. It is also included in the dialog history.       |
| memory_num       | int             | Maximum number of utterances in the dialog history stored by the system.                 |
| use_cuda         | -               | This option enables the GPU for faster inference with FP16.                              |

```
python run.py --mode cli \
    --check_point_path ./checkpoints/best_model.pt
    --dict_dir ./data/sample/
    --spm_model_path ./data/spk32.model
    --system_name Siri
    --initial_message Hello
    --memory_num 4
    --use_cuda
```


## License

This software is released under the MIT License, see LICENSE.txt.

## Contacts

Twitter: [@ryu1104_m](https://twitter.com/ryu1104_m)

Mail: ryu1104.as[at]gmail.com
