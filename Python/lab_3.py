from PIL import Image
import os

def read_coordinates(keys_file):
    coordinates = []
    with open(keys_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('(') and line.endswith(')'):
                # Парсинг координат вида (73, 175)
                coords = line[1:-1].split(',')
                x = int(coords[0].strip())
                y = int(coords[1].strip())
                coordinates.append((x, y))
    return coordinates

def decode_message(image_path, coordinates):
    img = Image.open(image_path)
    pixels = img.load()
    decoded_bytes = bytearray()
    
    for x, y in coordinates:
        try:
            pixel = pixels[x, y]
            if len(pixel) >= 3:
                blue_val = pixel[2]
                if blue_val == 0:  # Нулевой терминатор = конец сообщения
                    break
                decoded_bytes.append(blue_val)
        except (IndexError, TypeError):
            break
            
    return decoded_bytes.decode('utf-8', errors='ignore')

def encode_message(image_path, output_path, message, coordinates):
    img = Image.open(image_path)
    pixels = img.load()
    message_bytes = message.encode('utf-8')
    
    verification_info = {
        'first_char_bits': None,
        'original_pixels': [],
        'modified_pixels': []
    }
    
    if message_bytes:
        verification_info['first_char_bits'] = format(message_bytes[0], '08b')
    
    # 1. Записываем байты сообщения
    for i, byte_value in enumerate(message_bytes):
        if i >= len(coordinates):
            break
        x, y = coordinates[i]
        try:
            original_pixel = list(pixels[x, y])
            verification_info['original_pixels'].append({'coords': (x, y), 'pixel': tuple(original_pixel)})
            
            modified_pixel = original_pixel.copy()
            modified_pixel[2] = byte_value
            verification_info['modified_pixels'].append({'coords': (x, y), 'pixel': tuple(modified_pixel)})
            
            pixels[x, y] = tuple(modified_pixel)
        except (IndexError, TypeError):
            break
            
    # 2. Очищаем оставшиеся пиксели нулями (терминатор)
    for i in range(len(message_bytes), len(coordinates)):
        x, y = coordinates[i]
        try:
            pixel = list(pixels[x, y])
            pixel[2] = 0
            pixels[x, y] = tuple(pixel)
        except:
            break
            
    img.save(output_path)
    return verification_info

def display_verification_info(info):
    print("ПРОВЕРОЧНАЯ ИНФОРМАЦИЯ")
    
    print("a. Биты первого символа текстового сообщения:")
    print(f"   {info['first_char_bits']}")
    
    print("b. Исходные значения пикселей (первые 5):")
    for i, pixel_info in enumerate(info['original_pixels'][:5]):
        print(f"   Пиксель {i+1} по координатам {pixel_info['coords']}: RGB{pixel_info['pixel']}")
    
    print("c. Изменённые значения пикселей (первые 5):")
    for i, pixel_info in enumerate(info['modified_pixels'][:5]):
        print(f"   Пиксель {i+1} по координатам {pixel_info['coords']}: RGB{pixel_info['pixel']}")
    

def main():
    # Пути к файлам
    keys_file = "keys21.txt"
    encoded_image = "new21.png"  # Имя закодированного изображения
    new_encoded_image = "encoded_output.png"  # Имя нового закодированного изображения
    
    coordinates = read_coordinates(keys_file)
    print(f"Загружено координат: {len(coordinates)}")
    
    # Задание 1.1: Декодирование сообщения
    print("Задание 1.1: Декодирование сообщения")
    
    try:
        decoded_message = decode_message(encoded_image, coordinates)
        print(f"Декодированное сообщение: {decoded_message}\n")
        
    except FileNotFoundError:
        print(f"Ошибка: Закодированное изображение '{encoded_image}' не найдено!")
        print("Пожалуйста, убедитесь, что файл new21.png находится в той же папке")
    
    # Задание 1.2: Кодирование сообщения
    print("Задание 1.2: Кодирование сообщения")
    
    message_to_encode = "Привет, Мир!"
    print(f"Сообщение для кодирования: {message_to_encode}")
    
    try:
        verification_info = encode_message(
            encoded_image, 
            new_encoded_image, 
            message_to_encode, 
            coordinates
        )
        
        # Отображение проверочной информации
        display_verification_info(verification_info)
        
        print("Закодированное изображение сохранено как:", new_encoded_image)
        
        # Проверка путём декодирования
        print("Проверка кодирования путём декодирования...")
        verified_message = decode_message(new_encoded_image, coordinates)
        print(f"Раскодировано для проверки: {verified_message}")
        
    except FileNotFoundError:
        print(f"Ошибка: Исходное изображение '{encoded_image}' не найдено!")
        print("Пожалуйста, убедитесь, что файл new21.png существует")

if __name__ == "__main__":
    main()