
// FILE MODEL

 // Khai bao Du lieu
 {string} Warehouses = ...;
 {string} Customers = ...;
 int Demand[Customers]= ...;
 float Distance[Warehouses][Customers]=...;
 float FixedCost[Warehouses] =...; 
 float Capacity[Warehouses] =...; 
 
 // Khai bao Bien
 dvar boolean OpenWareHouse[Warehouses];
 dvar float+ ShiptoCustomer[Warehouses][Customers];
 
 // Khai bao ham muc tieu
 // Ham chi phi mo nha may
 dexpr float FacilityCost = sum(w in Warehouses) FixedCost[w]*OpenWareHouse[w];
 // Ham chi phi van chuyen
 dexpr float TransportCost = sum(c in Customers, w in Warehouses)(0.92*2/150*Demand[c]*Distance[w][c]*ShiptoCustomer[w][c]);
 
 // Ham muc tieu
 minimize FacilityCost + TransportCost;
 
 // Rang buoc
 subject to {

   // Khai bao rang buoc 1, tong luong van chuyen den 1 thi truong la 1
   forall (c in Customers)
     ctShip:
     sum(w in Warehouses)
       ShiptoCustomer[w][c]==1;
       
   // Rang buoc 2, Tong luong cung cap tu 1 nha may phai nho hon nang luc san xuat cua nha may do
    forall (w in Warehouses)
      ctShipOpen:
      sum(c in Customers)
        Demand[c]*ShiptoCustomer[w][c] <= Capacity[w]*OpenWareHouse[w];
//
//// Gioi han toi da khoang cach van chuyen la 70
//    forall (w in Warehouses, c in Customers:Distance[w][c]>=70)
//      ctShip70:
//      ShiptoCustomer[w][c]==0 ;

 } 
 
 