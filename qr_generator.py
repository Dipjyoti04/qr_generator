import qrcode

#______________________________________________________________________________________
#This script only uses the TERMINAL for URL and QR_NAME as input. see the TERMINAl :-)
#If you found this useful buy me a coffe 😉🍵
#--------------------------------------------------------------------------------------

def main():
    data = input("Enter the data or URL : ").strip()
    if not data:
        print("No input provided. Exiting.")
        return

    filename = input("Enter the filename (without .png): ").strip()
    if not filename:
        print("No filename provided. Exiting.")
        return

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    file_path = f"{filename}.png"
    img.save(file_path)

    print(f"QR code saved successfully in'{file_path}'")

if __name__ == "__main__":
    main()
