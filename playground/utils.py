import os

def norm(n: int, length: int = 3):
    if length < len(str(n)):
        return str(n)
    return '0' * (length -len(str(n))) + str(n)


def rename_images():
    people = ['abil', 'adilkhan', 'adnan', 'alisher', 'aslan', 'assiya', 'dana', \
                'daniyar', 'demirci', 'maxim', 'mikhail', 'mukhit', 'nazerke', \
                'oleg', 'zhanibek']
    for name in people:
        folder = f'/home/zhanibek/datasets/students_aligned/{name}'
        i = 1
        for filename in os.listdir(folder):
            person = folder.split('/')[-1]
            new_name = ''.join([person, '_', norm(i), ".png"])
            src = os.path.join(folder, filename)
            dst = os.path.join(folder, new_name)
            os.rename(src, dst)
            i += 1


if __name__ == '__main__':
    rename_images()
