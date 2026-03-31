import wave
import numpy as np
import matplotlib.pyplot as plt
import time
from pathlib import Path


def read_wav_file(filename, num_samples_requested):
    # Чтение дискретных отсчётов из WAV-файла.
    with wave.open(filename, 'rb') as wav_file:
        # Проверка формата файла
        if wav_file.getsampwidth() != 2:
            raise ValueError(f"Ожидается 16-bit PCM, получено {wav_file.getsampwidth()*8}-bit")
        if wav_file.getnchannels() != 1:
            raise ValueError(f"Ожидается моно, получено {wav_file.getnchannels()} каналов")
        
        sample_rate = wav_file.getframerate()
        
        # Чтение всех кадров и преобразование в массив чисел
        frames = wav_file.readframes(wav_file.getnframes())
        signal = np.frombuffer(frames, dtype=np.int16).astype(np.float64)
        
        # Ограничение количества отсчётов по запросу пользователя
        if num_samples_requested > len(signal):
            print(f"Предупреждение: в файле только {len(signal)} отсчётов. "
                  f"Используется всё содержимое.")
            num_samples_requested = len(signal)
        
        return signal[:num_samples_requested], sample_rate


def compute_dft_magnitude(signal):
    # Вычисление модуля ДПФ
    N = len(signal)
    
    # Быстрое вычисление ДПФ через FFT
    spectrum = np.fft.fft(signal)
    
    # Модуль комплексного спектра
    magnitude = np.sqrt(spectrum.real**2 + spectrum.imag**2)
    
    # Частотная ось
    frequencies = np.fft.fftfreq(N, d=1/32000)[:N//2]
    
    # Возвращаем только первую половину спектра
    return magnitude[:N//2], frequencies


def plot_oscillogram(signal, sample_rate, save_path='oscillogram.png'):
    # Построение осциллограммы
    # Временная ось
    time_axis = np.arange(len(signal)) / sample_rate
    
    plt.figure(figsize=(12, 4))
    plt.plot(time_axis, signal, linewidth=0.5, color='#2E86AB', label='Звуковой сигнал')
    
    plt.xlabel('Время, с', fontsize=11)
    plt.ylabel('Амплитуда, у.е.', fontsize=11)
    plt.title('Осциллограмма звукового сигнала', fontsize=13, fontweight='bold')
    
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(loc='upper right', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Осциллограмма сохранена: {save_path}")
    plt.show()


def plot_spectrum(magnitude, frequencies, save_path='spectrum.png'):
    # Спектральный анализ: график модуля ДПФ в зависимости от частоты.
    # Нормализация спектра для наглядности
    if np.max(magnitude) > 0:
        magnitude_normalized = magnitude / np.max(magnitude) * 100
    else:
        magnitude_normalized = magnitude
    
    plt.figure(figsize=(12, 4))
    plt.plot(frequencies, magnitude_normalized, linewidth=0.8, color='#A23B72', label='|X(k)| = √(Re² + Im²)')
    
    plt.xlabel('Частота, Гц', fontsize=11)
    plt.ylabel('Нормированная амплитуда, %', fontsize=11)
    plt.title('Спектральный анализ: модуль ДПФ звукового сигнала', fontsize=13, fontweight='bold')
    
    # Ограничение по теореме Найквиста
    plt.xlim(0, 16000)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(loc='upper right', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Спектр сохранён: {save_path}")
    plt.show()


def plot_histogram(signal, num_bins=50, save_path='histogram.png'):
    # Гистограмма распределения амплитуд отсчётов сигнала.
    plt.figure(figsize=(10, 5))
    
    # Построение гистограммы
    counts, bins, patches = plt.hist(signal, bins=num_bins, color='#06A77D', 
                                     edgecolor='black', alpha=0.8, density=False)
    
    plt.xlabel('Амплитуда сигнала, у.е.', fontsize=11)
    plt.ylabel('Количество отсчётов, шт.', fontsize=11)
    plt.title('Гистограмма распределения амплитуд звукового сигнала', fontsize=13, fontweight='bold')
    
    plt.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    stats_text = (f'Среднее: {np.mean(signal):.1f}\n'
                  f'Стд. откл.: {np.std(signal):.1f}\n'
                  f'Мин: {np.min(signal):.0f}\n'
                  f'Макс: {np.max(signal):.0f}')
    plt.text(0.98, 0.98, stats_text, transform=plt.gca().transAxes, 
             fontsize=9, verticalalignment='top', horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Гистограмма сохранена: {save_path}")
    plt.show()


def print_signal_info(signal, sample_rate):
    # Вывод основной информации о сигнале в консоль
    duration_ms = len(signal) / sample_rate * 1000
    nyquist_freq = sample_rate / 2
    
    print("\n" + "="*60)
    print("Информация о сигнале")
    print("="*60)
    print(f"Частота дискретизации:     {sample_rate} Гц")
    print(f"Количество отсчётов:       {len(signal)}")
    print(f"Длительность фрагмента:    {duration_ms:.1f} мс")
    print(f"Диапазон частот: 0 – {nyquist_freq:.0f} Гц")
    print(f"Диапазон амплитуд:         [{np.min(signal):.0f} ; {np.max(signal):.0f}] у.е.")
    print(f"Среднее значение:          {np.mean(signal):.2f} у.е.")
    print(f"Среднеквадратичное:        {np.std(signal):.2f} у.е.")
    print("="*60 + "\n")


def main():
    print("Обработка звукового сигнала")
    print("-" * 55)

    start_time = time.time()
    
    filename = input("Введите имя WAV-файла: ").strip()
    
    file_path = Path(filename)
    if not file_path.is_absolute():
        script_dir = Path(__file__).parent.resolve()
        file_path = script_dir / filename
    
    if not file_path.exists():
        print(f"Ошибка: файл '{file_path}' не найден!")
        return
    
    try:
        num_samples = int(input("Введите количество отсчётов для обработки: "))
        if num_samples <= 0:
            raise ValueError
    except ValueError:
        print("Ошибка: введите положительное целое число")
        return
    
    try:
        print(f"\nЧтение файла: {file_path.name}")
        signal, sample_rate = read_wav_file(str(file_path), num_samples)
        print(f"Загружено {len(signal)} отсчётов")
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        return
    
    print_signal_info(signal, sample_rate)
    
    print("Построение осциллограммы")
    plot_oscillogram(signal, sample_rate)
    
    print("Выполнение спектрального анализа (ДПФ)")
    magnitude, frequencies = compute_dft_magnitude(signal)
    plot_spectrum(magnitude, frequencies)
    
    print("Построение гистограммы амплитуд")
    plot_histogram(signal)

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print("\n" + "="*60)
    print(f"Время выполнения программы: {elapsed_time:.3f} секунд")
    print("="*60)
    
    print("Обработка завершена. Созданы файлы:")
    print("oscillogram.png — осциллограмма сигнала")
    print("spectrum.png — спектральный анализ")
    print("histogram.png — гистограмма амплитуд")


if __name__ == "__main__":
    main()
