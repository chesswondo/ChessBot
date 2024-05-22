# ChessBot

## About
ChessBot is a program that can easily recognize chess position from the screen in real-time mode.

Currently it provides you three modes which you can use:

1. You can choose the option to use stockfish 16.1 ([strong open source chess engine](https://stockfishchess.org/)) to analyze the position on your screen and to get suggestions about best move.
2. If you're tired of using mouse to make moves, you can choose the speech recognition option and make moves just calling them out loud in the format like e2e4.
ChessBot will make moves using your mouse automatically.
3. Currently last fun option is to use ChessBot as a real bot. You won't have to do anything, program will manage your pieces automatically using stockfish engine.

### Notice:

**Please, adhere to chess ethics and never use the last mode against other players. It is just for fun, not for trick.**

## Installation

#### 1. Clone the repository:
```bash
git clone https://github.com/chesswondo/ChessBot
```

#### 2. Navigate to projects directory:
```bash
cd ChessBot
```

Note that you will need to set pythonpath at this directory to use the modules.

You will also need to have conda installed on your system.
For more information, see
[conda documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/install/).

#### 3. Create an empty virtual environment with conda:
```bash
conda create --name chess_env python=3.11
```

Python version 3.11 is recommended to avoid errors with newer version 3.12.

#### 4. Activate the conda environment:
```bash
conda activate chess_env
```

#### 5. _[Install PyTorch 2.2.0](https://pytorch.org/get-started/previous-versions/#v220)_ according to your system.
[![link](assets/readme_images/pytorch_installation.png)](https://pytorch.org/get-started/previous-versions/#v220)

Pytorch version 2.2.0 is also recommended to avoid errors.

#### 6. Install Openmim (installation tool for MM libraries):
```bash
pip install openmim
```

#### 7. Install **MMCV**:
```bash
mim install mmcv
```

#### 8. Install **MMDetection**:
```bash
mim install mmdet
```

#### 9. Install the rest of the dependencies:
```bash
pip install -r requirements.txt
```

#### 10. Download stockfish:
To use stockfish chess engine, download it from the [official website](https://stockfishchess.org/download/) according to your system and put an executable file in the assets/models/chess_engine/stockfish folder.

## Run
To use the program, first navigate to project's directory. Than you can use the next script:
```bash
python ChessBot.py \
  <option> --monitor monitor_number
```

Here you can change the --monitor flag if you have access to several monitors and want to use an another one.

If it's not specified, program will use the default monitor.
So your default command to run the program will look just like this:
```bash
python ChessBot.py
```
