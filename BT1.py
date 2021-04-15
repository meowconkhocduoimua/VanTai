import heapq
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog
import csv

def TimViTriFile():
    root= tk.Tk()

    canvas1 = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue2', relief = 'raised')
    canvas1.pack()

    def getCSV ():
        ViTri = filedialog.askopenfilename()
        print(ViTri)
        return str(ViTri)
        # pass

        
    browseButton_CSV = tk.Button(text="      Import CSV File     ", command=getCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
    canvas1.create_window(150, 150, window=browseButton_CSV)
    return getCSV()
    root.mainloop()
    
    
# Kiểu nhập ma trận sẵn 
def NhapCSV(ViTri):
    with open(ViTri,encoding='utf-8') as file:
        # Cắt dữ liệu theo từng dòng, duyệt từng hàng
        data = file.read().split('\n')

    KhoangCach =[]
    for i in data:
        #  Tại dòng đầu tiên lấy ra danh sách bắt đầu, bỏ ô đầu tiên
        if data.index(i) ==0:
            i = i.split(',')
            DanhSachBatDau = i[1:]
        # Vì khi nhập sẽ có lỗi list rỗng
        elif i=="":
            pass
            
        else:
            i = i.split(',')
            # Tạo biến phụ a để xử lý theo hàng
            a =[]
            # Vì giá trị đầu mỗi hàng là vị trí nên k lấy giá trị đó vào ma trận
            for j in range(1,len(i)):
                # Nếu các ô trong excel nhập trống thì sẽ hiển thị list rỗng
                # Những cái list rỗng sẽ thêm số 0 vào
                if i[j] =='':
                    a.append(0)
                # Vì đọc từ csv là dạng chuỗi nên phải chuyển sang số nguyên
                else:
                    a.append(float(i[j]))
            # biến a là duyệt theo từng hàng, thêm vào ma trận khoảng cách từng list của a
            KhoangCach.append(a)      
    return KhoangCach, DanhSachBatDau

# Kiểu nhập kiểu QM, phải tạo lại ma trận
def NhapCSV2(ViTri):
    with open(ViTri,encoding='utf-8') as file:
        data = file.read().split('\n')
    a = []
    for i in data:
        if data.index(i) ==0:
            pass
        elif i=="":
            pass
        else:
            a.append(i.split(','))
    KhoangCach = []
    for i in range(36):
        KhoangCach.append([])
        for j in range(36):
            KhoangCach[i].append(0)
    DanhSachBatDau = []
    for i in a:
        # Bởi vì có thể đi 2 chiều nên tạo xuôi tạo ngược
        KhoangCach[int(i[1])][int(i[2])]= float(i[3])
        KhoangCach[int(i[2])][int(i[1])]= float(i[3])
        if i[0] !="":
            DanhSachBatDau.append(i[0])
    return KhoangCach, DanhSachBatDau
    
def ChuyenDoiMaTran(KhoangCach,DanhSachBatDau,DanhSachKetThuc):
    dct_SoDo = dict()
    for i in range(n):
        List_con = []
        for j in range(n):
            if KhoangCach[i][j] !=0:
                List_con.append((DanhSachKetThuc[j],KhoangCach[i][j]))
        dct_SoDo[DanhSachBatDau[i]]=List_con
    return(dct_SoDo)

def DuongDiNganNhat(SoDo,BatDau,KetThuc):
    DanhSach = []
    DanhSachNganNhat = []
    heapq.heappush(DanhSach,(0,BatDau,0))
    # print(h)
    # Tạo danh sách những điểm đã chiếm để k quay lại
    DanhSachDaChiem = []
    while len(DanhSach)!=0:
        #  Xem xét trong danh sách cái nào chi phí nhỏ nhất thì đem ra làm node hiện tại
        ChiPhiHienTai,NodeDangXet,NodeTruoc = heapq.heappop(DanhSach)
        # Thêm node có chi phí nhỏ nhất vào danh sách node đã chiếm
        DanhSachDaChiem.append(NodeDangXet)
        # Tạo biến đếm số lượng Node dang xét có nằm trong Node đã xét rồi không
        # Nếu trong danh sách có rồi
        # Thì không có thêm vào nữa vì đã xét rồi
        dem = 0
        for i in DanhSachNganNhat:
            if NodeDangXet == i[1]:
                dem += 1
        if dem == 0:
            heapq.heappush(DanhSachNganNhat,(ChiPhiHienTai,NodeDangXet,NodeTruoc))
        if NodeDangXet == KetThuc:
            KetLuan = "Khoảng cách từ {} đến {} là {}".format(BatDau,KetThuc,ChiPhiHienTai)
            # Trả về kết luận và danh sách đường đi ngắn nhất
            return KetLuan, DanhSachNganNhat
            break
        for HangXom,ChiPhiDenHangXom in SoDo[NodeDangXet]:
            if HangXom not in DanhSachDaChiem:
            # Push thêm vào danh sách những node hàng xóm với node đang xét
            #  Cập nhật chi phí: chi phí hiện tại của node đang xét + chi phí vận chuyển đến = chi phí mới của hàng xóm
            # Lưu lại vị trí hiện tại để biết chi phí của hàng xóm là do từ hướng nào tới
                heapq.heappush(DanhSach,(ChiPhiHienTai+ChiPhiDenHangXom,HangXom,NodeDangXet))
        
def NoiDiem(DanhSachNganNhat,BatDau,KetThuc):
    # Để truy lại đường đi ngắn nhất 
    # Ta truy từ dưới lên
    HienTai = KetThuc
    DuongDi = [KetThuc]
    while HienTai != BatDau:
        for i in DanhSachNganNhat:
            if HienTai == i[1]:
                HienTai = i[2]
                DuongDi.append(HienTai)
    # Vì là đi ngược, thêm vào cũng ngược nên là phải đảo ngược lại thì mới đi xuôi :v
    return DuongDi[::-1]

def CacKhoangCacConLai():
    print("Các khoảng cách ngắn nhất còn lại từ {} là: ".format(BatDau))
    DanhSachToaNha =[]
    for i in DanhSachKetThuc: 
        try:
            int(i)
        except:
            DanhSachToaNha.append(i)
    print(DanhSachNganNhat)
    for i in DanhSachToaNha:
        if i!= BatDau and i!= KetThuc:
            DuongDi = NoiDiem(DanhSachNganNhat,BatDau,i) 
            print(DuongDi)
            for j in DanhSachNganNhat:
                if i == j[1]:
                    print("Từ {} đến {} là: {} với khoảng cách là {}".format(BatDau,i,",".join(DuongDi),j[0]))
                    print(i)
                else:
                    pass
            else:
                pass
        else:
            pass
# Vị trí file CSV
ViTri = 'BAI1_SoLieuPython.csv'
# ViTri = TimViTriFile()

# Khai báo
KhoangCach, DanhSachBatDau = NhapCSV2(ViTri)
DanhSachKetThuc = DanhSachBatDau.copy()
n = len(DanhSachBatDau)

# Chuyển đổi dạng ma trận sang dict để quản lý
SoDo = ChuyenDoiMaTran(KhoangCach,DanhSachBatDau,DanhSachKetThuc)
# print(SoDo)
# Khai báo điểm bắt đầu và kết thúc
BatDau,KetThuc = ("34-C6","0-Cổng")

# Giải thuật tìm đường đi ngắn nhất, return ra Kết luận và DanhSachNganNhat
KetLuan, DanhSachNganNhat = DuongDiNganNhat(SoDo,BatDau,KetThuc)

# Từ Danh sách ngắn nhất dùng hàm để Đưa ra đường nối
DuongDi = NoiDiem(DanhSachNganNhat,BatDau,KetThuc)

print("Đường đi ngắn nhất từ {} đến {} là: {}".format(BatDau,KetThuc,",".join(DuongDi)))
print(KetLuan)

# CacKhoangCacConLai()
