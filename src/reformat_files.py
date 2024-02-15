import os 

def main(): 
    path = '../gbff/data'
    files = os.listdir(path)
    files = [os.path.join(path, file) for file in files]

    for i, file in enumerate(files): 
        name = None
        with open(file) as f:
            for line in f: 
                if name != None:
                    break
                if 'ORGANISM' in line: 
                    parse = line.strip().split('ORGANISM')
                    if len(parse) > 5: print(file)
                    for item in parse: 
                        if item == '' or len(item) < 1:
                            continue 
                        else: 
                            name = item.strip().replace(' ', '_').replace('.', '')
                    print(name)
            os.rename(file, f'{os.path.abspath(path)}/{name}.gbff')


if __name__ == '__main__':
    main()