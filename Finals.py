import pyodbc as odbc
from prettytable import PrettyTable
from tkinter import *
from tkinter import messagebox
from datetime import datetime

def shift_pegawai():
    # Menggunakan koneksi yang sudah ada
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Mengelola')

    # Membuat tabel dengan PrettyTable
    x = PrettyTable()
    column_names = [column[0] for column in cursor.description]
    x.field_names = column_names

    for row in cursor.fetchall():
        x.add_row(row)

    # Membuat window baru
    new_window = Toplevel(root)
    text = Text(new_window)
    text.insert('end', str(x))
    text.pack()

#Delete Data Customer
def update_data_mesin():
    update_window = Toplevel(root)
    update_window.title("Update Data Mesin")
    update_window.geometry("300x200")

    Label(update_window, text="Nama Mesin:").pack()
    nama_mesin_entry = Entry(update_window)
    nama_mesin_entry.pack()

    Label(update_window, text="Mesin digunakan?").pack()

    def update_status(status):
        cursor = conn.cursor()
        nama_mesin = nama_mesin_entry.get()
        cursor.execute(f"UPDATE dbo.TabelMesinCuci SET status = '{status}' WHERE nama = '{nama_mesin}'")
        conn.commit()
        if status == 'Occupied':
            messagebox.showinfo("Info", "Selamat Menggunakan!")
        else:
            messagebox.showinfo("Info", "Mesin di Reset, Terima Kasih!")

    Button(update_window, text="Ya", command=lambda: update_status('Occupied')).pack()
    Button(update_window, text="Tidak", command=lambda: update_status('Available')).pack()

def del_cust_data():
    def submit():
        cursor = conn.cursor()
        id = id_entry.get()
        cursor.execute(f"DELETE FROM TabelPelanggan WHERE id = {id}")
        conn.commit()
        messagebox.showinfo("Success", "Delete successful!")
        delete_window.destroy()

    delete_window = Toplevel(root)

    Label(delete_window, text="id").pack()
    id_entry = Entry(delete_window)
    id_entry.pack()

    Button(delete_window, text="Delete", command=submit).pack()

#Edit Data Customer
def edit_cust_data():
    def submit():
        cursor = conn.cursor()
        id = id_entry.get()
        updates = []
        if namaCustomer_entry.get():
            namaCustomer = namaCustomer_entry.get()
            updates.append(f"namaCustomer = '{namaCustomer}'")
        if HP_entry.get():
            HP = HP_entry.get()
            updates.append(f"HP = '{HP}'")
        if email_entry.get():
            email = email_entry.get()
            updates.append(f"email = '{email}'")
        if idKelurahan_entry.get():
            idKelurahan = idKelurahan_entry.get()
            updates.append(f"idKelurahan = {idKelurahan}")
        if updates:
            cursor.execute(f"UPDATE TabelPelanggan SET {', '.join(updates)} WHERE id = {id}")
            conn.commit()
            messagebox.showinfo("Success", "Update successful!")
        else:
            messagebox.showinfo("No changes", "No changes were made.")
        edit_window.destroy()

    edit_window = Toplevel(root)

    Label(edit_window, text="id").pack()
    id_entry = Entry(edit_window)
    id_entry.pack()

    Label(edit_window, text="Nama Customer (optional)").pack()
    namaCustomer_entry = Entry(edit_window)
    namaCustomer_entry.pack()

    Label(edit_window, text="HP (optional)").pack()
    HP_entry = Entry(edit_window)
    HP_entry.pack()

    Label(edit_window, text="Email (optional)").pack()
    email_entry = Entry(edit_window)
    email_entry.pack()

    Label(edit_window, text="id Kelurahan (optional)").pack()
    idKelurahan_entry = Entry(edit_window)
    idKelurahan_entry.pack()

    Button(edit_window, text="Update", command=submit).pack()

#Insert Data Customer
def insData_Customer_window():
    def submit():
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(id) FROM TabelPelanggan')
        max_id = cursor.fetchone()[0]
        id = max_id + 1 if max_id is not None else 1

        namaCustomer = namaCustomer_entry.get()
        HP = HP_entry.get()
        email = email_entry.get()
        idKelurahan = idKelurahan_entry.get()  # Mengambil idKelurahan

        cursor.execute('INSERT INTO TabelPelanggan(id, namaCustomer, HP, email, idKelurahan) VALUES(?,?,?,?,?);', (id, namaCustomer, HP, email, idKelurahan))
        conn.commit()
        success_message = f"Insert successful! id: {id}, Nama Customer: {namaCustomer}, HP: {HP}, Email: {email}, id Kelurahan: {idKelurahan}"
        messagebox.showinfo("Success", success_message)
        insert_window.destroy()

    insert_window = Toplevel(root)

    Label(insert_window, text="Nama Customer").pack()
    namaCustomer_entry = Entry(insert_window)
    namaCustomer_entry.pack()

    Label(insert_window, text="HP").pack()
    HP_entry = Entry(insert_window)
    HP_entry.pack()

    Label(insert_window, text="Email").pack()
    email_entry = Entry(insert_window)
    email_entry.pack()

    Label(insert_window, text="id Kelurahan").pack()  # Mengambil id Kelurahan
    idKelurahan_entry = Entry(insert_window)
    idKelurahan_entry.pack()

    Button(insert_window, text="Insert", command=submit).pack()

#Baca List Pelanggan
def customer_list_window():
    cursor = conn.cursor()
    cursor.execute("SELECT TabelPelanggan.id, namaCustomer, HP, email, namaKelurahan, namaKecamatan FROM TabelPelanggan JOIN TabelKelurahan ON TabelPelanggan.idKelurahan = TabelKelurahan.id JOIN TabelKecamatan ON TabelKelurahan.id = TabelKecamatan.id")

    table = PrettyTable()
    table.field_names = [column[0] for column in cursor.description]
    for row in cursor:
        table.add_row(row)

    new_window = Toplevel(root)
    new_window.title("List Pelanggan")
    new_window.geometry("800x800")

    text_widget = Text(new_window, wrap=WORD, state='disabled')
    text_widget.pack(expand=YES, fill=BOTH)

    text_widget.config(state='normal')
    text_widget.insert('end', str(table))
    text_widget.config(state='disabled')

#Baca Laporan Transaksi
def lap_transaksi_window():
    def filter_date():
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        cursor.execute(f"SELECT * FROM TabelTransaksi WHERE TanggalTransaksi BETWEEN '{start_date}' AND '{end_date}'")
        update_table()
        total_income()

    def reset_filter():
        cursor.execute("SELECT * FROM TabelTransaksi")
        update_table()
        total_income()

    def update_table():
        table.clear_rows()
        for row in cursor:
            table.add_row(row)
        text_widget.config(state='normal')
        text_widget.delete('1.0', END)
        text_widget.insert('end', str(table))
        text_widget.config(state='disabled')

    def total_income():
        cursor.execute("SELECT SUM(total) FROM TabelTransaksi")
        total = cursor.fetchone()[0]
        total_label.config(text=f"Total Penghasilan: Rp.{total}")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TabelTransaksi")

    table = PrettyTable()
    table.field_names = [column[0] for column in cursor.description]
    for row in cursor:
        table.add_row(row)

    new_window = Toplevel(root)
    new_window.title("Laporan Transaksi")
    new_window.geometry("1400x600")

    Label(new_window, text="Dari Tanggal:").pack()
    start_date_entry = Entry(new_window)
    start_date_entry.pack()

    Label(new_window, text="Sampai Tanggal:").pack()
    end_date_entry = Entry(new_window)
    end_date_entry.pack()

    Button(new_window, text="Filter", command=filter_date).pack()
    Button(new_window, text="Reset", command=reset_filter).pack()

    total_label = Label(new_window, text="")
    total_label.pack()
    Button(new_window, text="Hitung Total Penghasilan", command=total_income).pack()

    text_widget = Text(new_window, wrap=WORD, state='disabled')
    text_widget.pack(expand=YES, fill=BOTH)

    text_widget.config(state='normal')
    text_widget.insert('end', str(table))
    text_widget.config(state='disabled')

#Insert Data Transaksi
def insData_Transaksi_window():
    def submit():
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(id) FROM dbo.TabelTransaksi')
        max_id = cursor.fetchone()[0]
        id = max_id + 1 if max_id is not None else 1

        TanggalTransaksi = date_entry.get()
        WaktuMulai = datetime.strptime(start_time_entry.get(), '%H:%M:%S')
        WaktuSelesai = datetime.strptime(end_time_entry.get(), '%H:%M:%S')
        DurasiPemakaian = int((WaktuSelesai - WaktuMulai).total_seconds() / 60)
        idPelanggan = customer_id_entry.get()
        idPegawai = employee_id_entry.get()
        namaMesinCuci = machine_name_entry.get()
        cursor.execute('SELECT harga_per_15_menit FROM dbo.TabelMesinCuci WHERE Nama = ?', (namaMesinCuci,))
        harga_per_15_menit = cursor.fetchone()[0]
        total = (DurasiPemakaian / 15) * float(harga_per_15_menit)
        cursor.execute('INSERT INTO dbo.TabelTransaksi(id, TanggalTransaksi, WaktuMulai, WaktuSelesai, DurasiPemakaian, idPelanggan, idPegawai, namaMesinCuci, total) VALUES(?,?,?,?,?,?,?,?,?);', (id, TanggalTransaksi, WaktuMulai.strftime('%H:%M:%S'), WaktuSelesai.strftime('%H:%M:%S'), DurasiPemakaian, idPelanggan, idPegawai, namaMesinCuci, total))
        conn.commit()
        success_message = f"Insert successful! id: {id}, Tanggal Transaksi: {TanggalTransaksi}, Waktu Mulai: {WaktuMulai.time()}, Waktu Selesai: {WaktuSelesai.time()}, Durasi Pemakaian: {DurasiPemakaian}, id Pelanggan: {idPelanggan}, id Pegawai: {idPegawai}, Nama Mesin Cuci: {namaMesinCuci}, Total: {total}"
        messagebox.showinfo("Success", success_message)
        insert_window.destroy()

    insert_window = Toplevel(root)

    Label(insert_window, text="Tanggal Transaksi").pack()
    date_entry = Entry(insert_window)
    date_entry.pack()

    Label(insert_window, text="Waktu Mulai").pack()
    start_time_entry = Entry(insert_window)
    start_time_entry.pack()

    Label(insert_window, text="Waktu Selesai").pack()
    end_time_entry = Entry(insert_window)
    end_time_entry.pack()

    Label(insert_window, text="id Pelanggan").pack()
    customer_id_entry = Entry(insert_window)
    customer_id_entry.pack()

    Label(insert_window, text="id Pegawai").pack()
    employee_id_entry = Entry(insert_window)
    employee_id_entry.pack()

    Label(insert_window, text="Nama Mesin Cuci").pack()
    machine_name_entry = Entry(insert_window)
    machine_name_entry.pack()

    Button(insert_window, text="Insert", command=submit).pack()

# List Mesin
def list_mesin_window():
    cursor = conn.cursor()
    TABEL = 'TabelMesinCuci'
    cursor.execute(f"SELECT * FROM {TABEL}")

    table = PrettyTable()
    table.field_names = [column[0] for column in cursor.description]
    for row in cursor:
        table.add_row(row)

    new_window = Toplevel(root)
    new_window.title("List Mesin Cuci")
    new_window.geometry("600x600")

    text_widget = Text(new_window, wrap=WORD, state='disabled')
    text_widget.pack(expand=YES, fill=BOTH)

    text_widget.config(state='normal')
    text_widget.insert('end', str(table))
    text_widget.config(state='disabled')

#LOGOUT/LOGIN UNTUK STAFF
def logout():
    root.destroy()
    show_login_window()

def show_login_window():
    login_window = Tk()
    login_window.title("Login sebagai Staff")
    login_window.geometry("300x150")

    Label(login_window, text="Username").pack()
    id_entry = Entry(login_window)
    id_entry.pack()

    Label(login_window, text="Password").pack()
    password_entry = Entry(login_window, show='*')
    password_entry.pack()

    def validate_login():
        id = id_entry.get()
        password = password_entry.get()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM TabelPegawai WHERE id = ? AND password = ?", (id, password))
        result = cursor.fetchone()
        if result:
            login_window.destroy()
            main_window()
        else:
            messagebox.showerror("Error", "Invalid ID or password")

    Button(login_window, text="Login", command=validate_login).pack()

    login_window.mainloop()

#LOGOUT / LOGIN UNTUK CUSTOMER
def logout_for_cust():
    main_cust_window.destroy()
    show_login_window_for_cust()

def show_login_window_for_cust():
    login_window_cust = Tk()
    login_window_cust.title("Login sebagai Customer")
    login_window_cust.geometry("300x150")

    Label(login_window_cust, text="Username").pack()
    email_entry = Entry(login_window_cust)
    email_entry.pack()
    
    global customer_name

    def validate_login_for_cust():
        email = email_entry.get()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM TabelPelanggan JOIN TabelKelurahan ON TabelPelanggan.idKelurahan = TabelKelurahan.id JOIN TabelKecamatan ON TabelKelurahan.id = TabelKecamatan.id WHERE email = ?", (email,))
        result = cursor.fetchone()
        if result:
            global customer_name
            columns = [column[0] for column in cursor.description]
            result_dict = dict(zip(columns, result))
            customer_name = result_dict['namaCustomer']
            login_window_cust.destroy()
            main_window_for_cust()
        else:
            messagebox.showerror("Error", "Email / Customer doesn't exist!")

    Button(login_window_cust, text="Login", command=validate_login_for_cust).pack()

    login_window_cust.mainloop()

#Customer Page
def main_window_for_cust():
    global main_cust_window
    main_cust_window = Tk()
    main_cust_window.geometry("300x150")
    main_cust_window.title("Laundry Newci")  # Perbaikan di sini

    welcome_label = Label(main_cust_window, text="Welcome, " + customer_name, font=("Helvetica", 12, "bold"))
    welcome_label.place(relx=0, rely=0, anchor=NW)

    listMesin = Button(main_cust_window, text= "List Mesin Cuci", width= 15, height=3, command=list_mesin_window)
    listMesin.place(relx=0.5, rely=0.2, anchor=N)

    logoutButton = Button(main_cust_window, text="Logout", command=logout_for_cust)
    logoutButton.place(relx=0.7, rely=0.5, anchor=W)

    main_cust_window.mainloop()

#Page for Customer
def cust_window():
    show_login_window_for_cust()

# Staff Page
def main_window():
    global root
    root = Tk()
    root.title("Program DBMS Laundry Newci // Staff Page")
    root.geometry("400x800")

    listMesin = Button(root, text= "List Mesin Cuci", width= 15, height=3, command=list_mesin_window)
    listMesin.place(relx=0, rely=0, anchor=NW)

    updateMesin = Button(root, text= "Kelola Mesin", width= 15, height=3, command=update_data_mesin) 
    updateMesin.place(relx=0.5, rely=0, anchor=NW)

    shiftButton = Button(root, text= "List Pengelola Mesin", width= 15, height=3, command=shift_pegawai)
    shiftButton.place(relx=0.5, rely=0.1, anchor=N)

    rTButton = Button(root, text= "Laporan Transaksi", width= 15, height=3, command=lap_transaksi_window)
    rTButton.place(relx=0.5, rely=0.2, anchor=N)

    insertTransButton = Button(root, text= "Insert Data Transaksi", width= 15, height=3, command=insData_Transaksi_window)
    insertTransButton.place(relx=0.5, rely=0.3, anchor=N)

    editDataCust = Button(root, text= "List Customer", width= 17, height=3, command=customer_list_window)
    editDataCust.place(relx=0.5, rely=0.4, anchor=N)

    insDataCust = Button(root, text= "Insert Data Pelanggan", width= 17, height=3, command=insData_Customer_window)
    insDataCust.place(relx=0.5, rely=0.5, anchor=N)

    editDataCust = Button(root, text= "Edit Data Customer", width= 17, height=3, command=edit_cust_data)
    editDataCust.place(relx=0.5, rely=0.6, anchor=N)

    delDataCust = Button(root, text= "Delete Data Customer", width= 17, height=3, command=del_cust_data)
    delDataCust.place(relx=0.5, rely=0.7, anchor=N)

    logoutButton = Button(root, text="Logout", command=logout)
    logoutButton.place(relx=0.7, rely=0.85, anchor=W)

    root.mainloop()

#Page for Staff
def staff_window():
    show_login_window()

#Initial Page
def early_page():
    global root
    root = Tk()
    root.title("Program DBMS Laundry Newci")
    root.geometry("400x250")

    tombolCust = Button(root, text= "Login sebagai Pelanggan", width= 20, height=3, command=show_login_window_for_cust)
    tombolCust.place(relx=0.5, rely=0.1, anchor=N)

    tombolStaff = Button(root, text= "Login sebagai Staff", width= 20, height=3, command=staff_window)
    tombolStaff.place(relx=0.5, rely=0.4, anchor=N)

    root.mainloop()

#odbc-connection
try:
    conn = odbc.connect('Driver={SQL Server};' 
                        'Server=DESKTOP-533O0U3;'
                        'Database=LaundryNewci;' 
                        'Trusted_connection=yes;')
    early_page()

# Error Handler
except odbc.Error as ex:
    sqlstate = ex.args[1]
    print(f"The error '{sqlstate}' occurred.")