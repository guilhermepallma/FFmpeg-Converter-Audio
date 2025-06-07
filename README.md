<h1 align="center">
  AudioShift
</h1>
  <strong>Uma aplicação de desktop robusta e de alta performance para conversão de áudio em lote.</strong>
  Construída com Python e FFmpeg, sua arquitetura paralela foi projetada para extrair o máximo de desempenho de CPUs modernas, oferecendo uma experiência de usuário fluida, intuitiva e multilíngue.

<p></p>

<p align="center">
  <img alt="Licença MIT" src="https://img.shields.io/badge/license-MIT-blue.svg">
  <img alt="Python 3.8+" src="https://img.shields.io/badge/python-3.8+-blue.svg">
  <img alt="Plataforma" src="https://img.shields.io/badge/platform-Windows-lightgrey.svg">
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/guilhermepallma/FFmpeg-Converter-Audio/refs/heads/main/images/audioshift%20interface.png" alt="AudioShift Banner">
</p>

---

## Índice

- [✨ Principais Funcionalidades](#-principais-funcionalidades)
- [🛠️ Tecnológias (Stack)](#-tecnológias-(stack))
- [🚀 Guia de Início Rápido (Desenvolvedores)](#-guia-de-início-rápido-desenvolvedores)
  - [Pré-requisitos](#pré-requisitos)
  - [Guia de Instalação](#guia-de-instalação)
- [📦 Compilando um Executável (Distribuição)](#-compilando-um-executável-distribuição)
- [📄 Licença](#-licença)
- [🙏 Agradecimentos](#-agradecimentos)

---

## ✨ Principais Funcionalidades

* **⚡ Motor de Conversão Paralelo:** Utiliza todos os núcleos da CPU para processar múltiplos arquivos simultaneamente, reduzindo drasticamente o tempo de conversão.
* **📂 Conversão em Lote:** Selecione dezenas de arquivos e converta todos de uma só vez com as mesmas configurações.
* **🎶 Amplo Suporte a Formatos:** Converta facilmente entre os formatos de áudio mais populares, incluindo **MP3, AAC, WAV e FLAC**.
* **📈 Controle de Qualidade Total:**
    * Para MP3, utilize a codificação **VBR (Bitrate Variável)** para obter a melhor relação entre qualidade e tamanho de arquivo.
    * Defina bitrates constantes (ex: 320kbps), Sample Rate (até 192kHz) e profundidade de bits (Bit Depth, até 32-bit) para controle absoluto.
* **🌐 Interface Multilíngue:** Suporte completo para **Português** e **Inglês**, com tradução dinâmica da interface.
* **🖥️ GUI Intuitiva e Resiliente:** Interface gráfica amigável que bloqueia controles durante operações críticas para prevenir erros e exibe o progresso em uma janela de status centralizada.

---

## 🛠️ Tecnológias (Stack)

* **Linguagem Principal: Python 3**
    * Escolhido por sua simplicidade, ecossistema robusto e excelentes bibliotecas padrão, permitindo um desenvolvimento rápido e limpo.

* **Interface Gráfica: Tkinter (com `ttk`)**
    * Utiliza a biblioteca nativa do Python para criar uma GUI leve e responsiva, garantindo compatibilidade sem a necessidade de dependências pesadas. O uso de widgets `ttk` confere um visual moderno e nativo ao sistema operacional.

* **Motor de Conversão: FFmpeg**
    * O coração do AudioShift. Uma solução de multimídia completa, de código aberto, capaz de decodificar, codificar, transcodificar e processar praticamente qualquer formato de áudio. A aplicação o utiliza através de chamadas de subprocesso.

* **Arquitetura de Software:**
    * **Programação Orientada a Objetos (OOP):** Organiza o código de forma modular e escalável.
    * **Multithreading:** Essencial para a conversão paralela e para manter a interface gráfica responsiva durante o processamento.
    * **Separação de Responsabilidades (SoC):** A lógica da interface (GUI) é desacoplada da lógica de conversão (Core), facilitando a manutenção e a expansão do projeto.

---

## 🚀 Guia de Início Rápido (Desenvolvedores)

Se você deseja executar o projeto a partir do código-fonte, siga os passos abaixo.

### Pré-requisitos

* [Python 3.8+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/) para clonagem do repositório.

### Guia de Instalação

1.  **Clone o Repositório**
    Abra seu terminal e execute o comando:
    ```bash
    git clone [https://github.com/guilhermepallma/FFmpeg-Converter-Audio.git](https://github.com/guilhermepallma/FFmpeg-Converter-Audio.git)
    cd FFmpeg-Converter-Audio
    ```

2.  **Configure o FFmpeg**

    > ⚠️ **Passo Crucial:** O FFmpeg não é distribuído junto com o código-fonte devido ao seu tamanho e licença. A aplicação espera encontrá-lo em uma pasta específica.

    * **Baixe o FFmpeg:** Vá para o site oficial de builds, como o [**gyan.dev**](https://www.gyan.dev/ffmpeg/builds/) (recomendado para Windows), e baixe a versão `essentials`.
    * **Crie a Estrutura de Pastas:** Dentro da pasta do projeto, crie o seguinte caminho: `audio_converter/ffmpeg/`.
    * **Copie os Executáveis:** Descompacte o arquivo baixado, navegue até a pasta `bin/` e copie os arquivos `ffmpeg.exe` e `ffprobe.exe` para a pasta `ffmpeg` que você acabou de criar.

    A estrutura final deve ser esta:
    ```
    audio_converter/
    ├── ffmpeg/
    │   ├── ffmpeg.exe
    │   └── ffprobe.exe
    ├── gui.py
    ├── converter.py
    └── languages.py
    ```

3.  **Crie e Ative um Ambiente Virtual (Recomendado)**
    Isso isola as dependências do seu projeto do restante do sistema.
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Instale as Dependências**
    Este projeto utiliza apenas bibliotecas padrão do Python. **Nenhuma instalação via `pip` é necessária.**

5.  **Execute a Aplicação**
    Com o ambiente virtual ativado, execute o seguinte comando:
    ```bash
    python audio_converter/gui.py
    ```

---

## 📦 Compilando um Executável (Distribuição)

Para empacotar a aplicação em um único arquivo `.exe` autocontido (incluindo o FFmpeg) para fácil distribuição, utilize o PyInstaller.

1.  **Instale o PyInstaller**
    ```bash
    pip install pyinstaller
    ```

2.  **Execute o Comando de Empacotamento**
    Navegue até o diretório raiz do projeto (`FFmpeg-Converter-Audio/`) e execute o comando abaixo no terminal. Ele instrui o PyInstaller a criar um único arquivo executável, sem janela de console, e a incluir os binários do FFmpeg.

    ```bash
    pyinstaller --noconfirm --onefile --windowed --name AudioShift ^
    --add-binary="audio_converter/ffmpeg/ffmpeg.exe;ffmpeg" ^
    --add-binary="audio_converter/ffmpeg/ffprobe.exe;ffmpeg" ^
    audio_converter/gui.py
    ```
    * `--onefile`: Cria um único executável.
    * `--windowed`: Remove a janela do console ao executar.
    * `--add-binary`: Empacota os binários do FFmpeg na pasta correta dentro do executável.

3.  **Encontre o Executável**
    O seu programa final, `AudioShift.exe`, estará dentro da pasta `dist/` recém-criada.
    
---

## 🙏 Agradecimentos

* A equipe do **[FFmpeg](https://github.com/FFmpeg/FFmpeg)** por criar e manter uma ferramenta de multimídia tão poderosa e versátil.
* A todos os contribuidores e à comunidade de código aberto.
