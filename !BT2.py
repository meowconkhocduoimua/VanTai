from docplex.mp.model import Model

import pandas as pd

mdl = Model(name="BTL")

# Nhập dữ liệu từ file Excel
Data = pd.read_excel (r'dataSESC.xlsx')
DataDemand = pd.DataFrame(Data, columns= ['Demand'])
DataFixcost = pd.DataFrame(Data, columns= ['Fixcost'])
DataCapacity = pd.DataFrame(Data, columns= ['Capacity'])
DataWarehouse = pd.DataFrame(Data, columns= ['Warehouses'])
DataCustomers = pd.DataFrame(Data, columns= ['Customers'])

# Khởi tạo các biến ở dạng list
Demand = []
Fixcost = []
Capacity = []
Warehouses = []
Customers = []
Distance = []
# Duyệt ma trận theo cột
for i in range(len(pd.DataFrame(Data, columns= ['Demand']))):
    if str(DataDemand.iat[i,0]) != "nan":
        Demand.append(DataDemand.iat[i,0])  
for i in range(len(pd.DataFrame(Data, columns= ['Fixcost']))):
    Fixcost.append(DataFixcost.iat[i,0])
for i in range(len(pd.DataFrame(Data, columns= ['Capacity']))):
    Capacity.append(DataCapacity.iat[i,0])
for i in range(len(pd.DataFrame(Data, columns= ['Warehouse']))):
    Warehouses.append(DataWarehouse.iat[i,0])
for i in range(len(pd.DataFrame(Data, columns= ['Customers']))):
    if str(DataCustomers.iat[i,0]) != "nan":
        Customers.append(DataCustomers.iat[i,0])  

for i in Customers:
    test = pd.DataFrame(Data, columns= [i])
    # a là biến giả để tạo list
    a =[]
    for i in range(len(pd.DataFrame(test, columns= [i]))):
        a.append(test.iat[i,0])  
    Distance.append(a)
#  Vì Excel duyệt theo cột nên ma trận tạo ra bị đảo ngược nên cần phải đảo ngược lại 
# Đảo ngược ma trận
Distance = [[Distance[j][i] for j in range(len(Distance))] for i in range(len(Distance[0]))]
n = len(Warehouses)
m = len(Customers)
def ChuyenDoiMaTran(Distance,Warehouse,Customers):
    dct_graph = dict()
    for i in range(n):
        dict_con = dict()
        for j in range(m):
            dict_con[Customers[j]]=Distance[i][j]
        dct_graph[Warehouse[i]]=dict_con
    return dct_graph
# Chuyển các biến thành dạn dict để tham chiếu
Demand = { Customers[i]:Demand[i] for i in range(len(Demand))}
Distance =ChuyenDoiMaTran(Distance,Warehouses,Customers)
Fixcost = {Warehouses[i]:Fixcost[i] for i in range(len(Fixcost))}
Capacity = {Warehouses[i]:Capacity[i]for i in range(len(Capacity))} 

# Khai báo biến
Openwarehouses= mdl.binary_var_dict(Warehouses,name="w")
Ship = [(i,j) for i in Warehouses for j in Customers]
ShipToCustomer = mdl.integer_var_dict(Ship,name='s')
# Khai báo hàm mục tiêu
FacilityCost = mdl.sum(Fixcost[w]*Openwarehouses[w] for w in Warehouses)
TransportCost = mdl.sum(Demand[c]*ShipToCustomer[w,c]*0.92*2*Distance[w][c]/150 for w in Warehouses for c in Customers )
# Cực tiểu hàm mục tiêu
mdl.minimize(FacilityCost+TransportCost)
# Thêm Ràng buộc
mdl.add_constraints(mdl.sum(ShipToCustomer[w,c] for w in Warehouses ) == 1 for c in Customers)
mdl.add_constraints(mdl.sum(ShipToCustomer[w,c]*Demand[c] for c in Customers ) <= Capacity[w]*Openwarehouses[w] for w in Warehouses)
# Ràng buộc những nơi có khoảng cách lớn hơn 70 sẽ không được vận chuyển
mdl.add_constraints(ShipToCustomer[w,c]==0 for w in Warehouses for c in Customers if Distance[w][c]>=70)
# mdl.parameters.timelimit = 15
sol = mdl.solve()
sol.display()