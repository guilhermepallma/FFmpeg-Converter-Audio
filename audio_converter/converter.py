import sys
import os
import subprocess
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

FORMAT_OPTIONS = {
    'MP3': {'bitrate': [('VBR (Máxima Qualidade)', '-q:a 0'), ('320 kbps', '-b:a 320k'), ('256 kbps', '-b:a 256k'), ('192 kbps', '-b:a 192k')], 'codec': 'libmp3lame'},
    'AAC': {'bitrate': [('320 kbps', '-b:a 320k'), ('256 kbps', '-b:a 256k'), ('192 kbps', '-b:a 192k'), ('128 kbps', '-b:a 128k')], 'samplerate': [('44100 Hz', '44100'), ('48000 Hz', '48000')], 'codec': 'aac'},
    'WAV': {'samplerate': [('192000 Hz', '192000'), ('96000 Hz', '96000'), ('48000 Hz', '48000'), ('44100 Hz', '44100')], 'bitdepth': [('32-bit', '32'), ('24-bit', '24'), ('16-bit', '16')]},
    'FLAC': {'samplerate': [('192000 Hz', '192000'), ('96000 Hz', '96000'), ('48000 Hz', '48000'), ('44100 Hz', '44100')], 'bitdepth': [('24-bit', '24'), ('16-bit', '16')], 'codec': 'flac'}
}

class ConversionLogic:
    def __init__(self, ffmpeg_path, ffprobe_path):
        self.ffmpeg_path = ffmpeg_path
        self.ffprobe_path = ffprobe_path
        self.max_workers = os.cpu_count() or 1

    def _get_ffmpeg_value(self, option_list, display_text):
        for display, value in option_list:
            if display == display_text: return value.split()
        return None

    def _build_ffmpeg_command(self, input_file, output_file, conversion_params):
        selected_format = conversion_params['format']
        command = [self.ffmpeg_path, '-y', '-i', input_file, '-vn']
        if conversion_params['is_stream_copy']:
            command.extend(['-c:a', 'copy'])
        else:
            options = FORMAT_OPTIONS.get(selected_format, {})
            codec = options.get('codec')
            if selected_format == 'WAV':
                depth_value = self._get_ffmpeg_value(options['bitdepth'], conversion_params['bitdepth'])
                if depth_value: codec = f'pcm_s{depth_value[0]}le'
            if codec: command.extend(['-acodec', codec])
            if 'bitrate' in options and conversion_params.get('bitrate'):
                bitrate_value = self._get_ffmpeg_value(options['bitrate'], conversion_params['bitrate'])
                if bitrate_value: command.extend(bitrate_value)
            if 'samplerate' in options and conversion_params.get('samplerate'):
                samplerate_value = self._get_ffmpeg_value(options['samplerate'], conversion_params['samplerate'])
                if samplerate_value: command.extend(['-ar', samplerate_value[0]])
        command.append(output_file)
        return command

    def _convert_single_file(self, task_params):
        input_file = task_params['input_file']
        output_file = task_params['output_file']
        conversion_params = task_params['conversion_params']
        try:
            command = self._build_ffmpeg_command(input_file, output_file, conversion_params)
            process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, universal_newlines=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            _, stderr_output = process.communicate()
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, command, stderr=stderr_output)
            return {'status': 'success', 'file': os.path.basename(input_file)}
        except Exception as e:
            return {'status': 'error', 'file': os.path.basename(input_file), 'error': e}

    def run_conversion(self, conversion_params, app_queue):
        output_base_dir = conversion_params['output_dir']
        output_folder_name = conversion_params['folder_name'].strip() or f"converted_{datetime.now().strftime('%d-%m-%y')}"
        final_output_path = os.path.join(output_base_dir, output_folder_name)
        os.makedirs(final_output_path, exist_ok=True)
        
        input_files = conversion_params['input_files']
        total_files = len(input_files)
        tasks = []
        for input_file in input_files:
            file_name_no_ext = os.path.splitext(os.path.basename(input_file))[0]
            output_file = os.path.join(final_output_path, f"{file_name_no_ext}.{conversion_params['format'].lower()}")
            tasks.append({'input_file': input_file, 'output_file': output_file, 'conversion_params': conversion_params})

        app_queue.put({'type': 'batch_start', 'total': total_files})
        completed_count = 0
        success_count = 0
        errors = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_task = {executor.submit(self._convert_single_file, task): task for task in tasks}
            for future in as_completed(future_to_task):
                completed_count += 1
                result = future.result()
                if result['status'] == 'error':
                    errors.append(f"{result['file']}: {result['error']}")
                else:
                    success_count += 1
                progress = (completed_count / total_files) * 100
                
                # --- LINHA CORRIGIDA ---
                # Enviando dados estruturados em vez de uma string formatada
                app_queue.put({
                    'type': 'total_progress',
                    'value': progress,
                    'current': completed_count,
                    'total': total_files,
                    'filename': result['file']
                })

        app_queue.put({'type': 'done', 'errors': errors, 'path': final_output_path, 'success_count': success_count})