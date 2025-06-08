STRINGS = {
    'pt': {
        # Títulos
        'window_title': "AudioShift",
        'progress_window_title': "Progresso da Conversão",
        # Labels dos Frames
        'section1_title': "1. Selecione os Arquivos de Áudio",
        'section2_title': "2. Escolha as Opções de Conversão",
        'section3_title': "3. Defina o Destino",
        # Botões
        'select_files_btn': "Adicionar Arquivos...",
        'select_folder_btn': "Adicionar Pasta...",
        'clear_list_btn': "Limpar Lista",
        'browse_btn': "Procurar...",
        'start_conversion_btn': "Iniciar Conversão",
        'close_btn': "Fechar",
        # Opções de Conversão
        'output_format_lbl': "Formato de Saída:",
        'preserve_quality_chk': "Mudar apenas o formato (preservar qualidade original)",
        'quality_bitrate_lbl': "Qualidade/Bitrate:",
        'samplerate_lbl': "Sample Rate:",
        'bitdepth_lbl': "Bit Depth:",
        # Destino
        'save_to_lbl': "Salvar em:",
        'output_folder_name_lbl': "Nome da Pasta de Saída (Opcional):",
        # Status e Progresso
        'progress_status_lbl': "Progresso Geral:",
        'status_waiting': "Aguardando início...",
        'status_starting': "Iniciando...",
        'status_converting': "Convertendo {current}/{total}: {filename}",
        'status_done': "Conversão Concluída!",
        # Menus
        'menu_language': "Idioma",
        # Mensagens de Erro e Sucesso
        'error_title': "Erro",
        'warning_title': "Aviso",
        'success_title': "Sucesso",
        'invalid_op_title': "Operação Inválida",
        'dest_required_title': "Destino Obrigatório",
        'no_files_selected_msg': "Nenhum arquivo selecionado para conversão.",
        'dest_required_msg': "Por favor, selecione uma pasta de destino clicando em 'Procurar...'.",
        'invalid_op_msg': "A opção 'Preservar qualidade original' não pode ser usada para converter para o formato {format}.",
        'conversion_success_msg': "Todos os {count} arquivos foram convertidos com sucesso em:\n{path}",
        'conversion_error_msg': "{count} arquivos convertidos com sucesso, mas ocorreram falhas:\n\n{errors}",
        'folder_ignored_warning_title': "Pasta Ignorada",
        'folder_ignored_warning_msg': "A pasta selecionada não contém arquivos de áudio suportados e foi ignorada:\n\n{folder}",
        'skipped_folders_msg': "\n\nAtenção: As seguintes pastas foram ignoradas por não conterem arquivos de áudio suportados:\n- {folders}",
        'progress_status_lbl': "Progresso Geral:",
        'etr_label': "Tempo Restante:",
        'etr_calculating': "Calculando...",
        'status_waiting': "Aguardando início...",
        'status_starting': "Iniciando...",
        'status_converting': "Convertendo {current}/{total}: {filename}",
        'status_done': "Conversão Concluída!",
        # ... (restante das strings) ...
                # ... (strings existentes) ...
        'preserve_quality_chk': "Mudar apenas o formato (preservar qualidade original)",
        'stream_copy_help_title': "Ajuda: Preservar Qualidade Original",
        'stream_copy_help_msg': "Esta opção, conhecida como 'cópia de fluxo', apenas reempacota o áudio sem recodificá-lo. Isso só é possível se o codec de áudio original for compatível com o formato final.\n\nOs formatos MP3 e AAC possuem codecs próprios e bem definidos. Para converter um arquivo de áudio (como .WAV ou .FLAC) para .MP3 ou .AAC, é obrigatório recodificar o áudio. Por esse motivo, a cópia de fluxo não é aplicável e a opção fica desabilitada.",
        'quality_bitrate_lbl': "Qualidade/Bitrate:",
        # ... (restante das strings) ...
    },
    'en': {
        # Titles
        'window_title': "AudioShift",
        'progress_window_title': "Conversion Progress",
        # Frame Labels
        'section1_title': "1. Select Audio Files",
        'section2_title': "2. Choose Conversion Options",
        'section3_title': "3. Set Destination",
        # Buttons
        'select_files_btn': "Add Files...",
        'select_folder_btn': "Add Folder...",
        'clear_list_btn': "Clear List",
        'browse_btn': "Browse...",
        'start_conversion_btn': "Start Conversion",
        'close_btn': "Close",
        # Conversion Options
        'output_format_lbl': "Output Format:",
        'preserve_quality_chk': "Change container only (preserve original quality)",
        'quality_bitrate_lbl': "Quality/Bitrate:",
        'samplerate_lbl': "Sample Rate:",
        'bitdepth_lbl': "Bit Depth:",
        # Destination
        'save_to_lbl': "Save to:",
        'output_folder_name_lbl': "Output Folder Name (Optional):",
        # Status and Progress
        'progress_status_lbl': "Overall Progress:",
        'status_waiting': "Waiting to start...",
        'status_starting': "Starting...",
        'status_converting': "Converting {current}/{total}: {filename}",
        'status_done': "Conversion Complete!",
        # Menus
        'menu_language': "Language",
        # Error and Success Messages
        'error_title': "Error",
        'warning_title': "Warning",
        'success_title': "Success",
        'invalid_op_title': "Invalid Operation",
        'dest_required_title': "Destination Required",
        'no_files_selected_msg': "No files selected for conversion.",
        'dest_required_msg': "Please select a destination folder by clicking 'Browse...'.",
        'invalid_op_msg': "The 'Preserve original quality' option cannot be used to convert to the {format} format.",
        'conversion_success_msg': "All {count} files were successfully converted in:\n{path}",
        'conversion_error_msg': "{count} files converted successfully, but failures occurred:\n\n{errors}",
        'folder_ignored_warning_title': "Folder Skipped",
        'folder_ignored_warning_msg': "The selected folder contains no supported audio files and was skipped:\n\n{folder}",
        'skipped_folders_msg': "\n\nNote: The following folders were skipped because they did not contain supported audio files:\n- {folders}",
        'progress_status_lbl': "Overall Progress:",
        'etr_label': "Time Remaining:",
        'etr_calculating': "Calculating...",
        'status_waiting': "Waiting to start...",
        'status_starting': "Starting...",
        'status_converting': "Converting {current}/{total}: {filename}",
        'status_done': "Conversion Complete!",
        # ... (rest of the strings) ...
        # ... (existing strings) ...
        'preserve_quality_chk': "Change container only (preserve original quality)",
        'stream_copy_help_title': "Help: Preserve Original Quality",
        'stream_copy_help_msg': "This option, also known as 'stream copy', only repackages the audio without re-encoding it. This is only possible if the original audio codec is compatible with the final container format.\n\nMP3 and AAC formats have their own specific codecs. To convert an audio file (like .WAV or .FLAC) to .MP3 or .AAC, the audio must be re-encoded. For this reason, stream copy is not applicable, and the option is disabled.",
        'quality_bitrate_lbl': "Quality/Bitrate:",
        # ... (rest of the strings) ...
    }
}