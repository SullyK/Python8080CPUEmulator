

x = 0x20
def test(x):
    match x:
        case 20:
            print("wronggg")
            return 
        case 0x20:
            print("nice")
            return

test(x)