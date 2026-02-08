CREATE
(cuto:Person {name:"CỤ TỔ"}),
(chitruong:Person {name:"CHI TRƯỜNG"}),
(hien:Person {name:"HIÊN"}),
(mau:Person {name:"MẬU"}),
(tuan:Person {name:"TUẤN"}),

(dai:Person {name:"ĐẠI"}),
(hoan:Person {name:"HOAN"}),

(tich:Person {name:"TÍCH"}),
(ich:Person {name:"ÍCH"}),

(tang:Person {name:"TĂNG"}),
(tai:Person {name:"TÀI"}),

(hai:Person {name:"HẢI"}),
(hoi:Person {name:"HỘI"}),
(thu:Person {name:"THU"}),
(nhap:Person {name:"NHẬP"}),

(kien:Person {name:"KIÊN"}),
(quan:Person {name:"QUÂN"}),
(duc:Person {name:"ĐỨC"}),
(nam1:Person {name:"NAM"}),
(long1:Person {name:"LONG"}),

(phung:Person {name:"PHÙNG"}),
(quang1:Person {name:"QUANG"}),
(anh1:Person {name:"ANH"}),
(linh:Person {name:"LINH"}),

(khoan:Person {name:"KHOAN"}),
(vuon:Person {name:"VƯƠN"}),

(can:Person {name:"CẨN"}),
(khai:Person {name:"KHẢI"}),

(don:Person {name:"ĐÔN"}),
(luan:Person {name:"LUÂN"}),
(thuy:Person {name:"THÚY"}),

(kinh:Person {name:"KÍNH"}),
(tinh:Person {name:"TÍNH"}),
(hoan2:Person {name:"HOÀN"}),

(cuong:Person {name:"CƯỜNG"}),
(son:Person {name:"SƠN"}),
(hoang:Person {name:"HOÀNG"}),

(luu:Person {name:"LƯU"}),
(luyen:Person {name:"LUYẾN"}),
(lieu:Person {name:"LIỄU"}),
(lien:Person {name:"LIÊN"}),
(nam2:Person {name:"NĂM"}),
(vinh1:Person {name:"VINH"}),
(huong:Person {name:"HƯƠNG"}),

(long2:Person {name:"LONG"}),
(thang:Person {name:"THẮNG"}),
(nam3:Person {name:"NAM"}),
(quang2:Person {name:"QUANG"}),
(giang:Person {name:"GIANG"}),
(lam:Person {name:"LÂM"}),

(ca:Person {name:"CA"}),
(tung:Person {name:"TÙNG"}),
(vu:Person {name:"VŨ"}),

(vinh2:Person {name:"VĨNH"}),
(hung:Person {name:"HÙNG"}),

(bao:Person {name:"BẢO"}),
(bang:Person {name:"BẰNG"}),
(dung:Person {name:"DŨNG"}),

// root
(cuto)-[:PARENT_OF {order:1}]->(chitruong),

// level 1
(chitruong)-[:PARENT_OF {order:1}]->(hien),
(chitruong)-[:PARENT_OF {order:2}]->(mau),
(chitruong)-[:PARENT_OF {order:3}]->(tuan),

// HIÊN branch
(hien)-[:PARENT_OF {order:1}]->(dai),
(hien)-[:PARENT_OF {order:2}]->(hoan),

(dai)-[:PARENT_OF {order:1}]->(tich),
(dai)-[:PARENT_OF {order:2}]->(ich),

(tich)-[:PARENT_OF {order:1}]->(tang),
(tang)-[:PARENT_OF {order:1}]->(tai),

(tai)-[:PARENT_OF {order:1}]->(hai),
(tai)-[:PARENT_OF {order:2}]->(hoi),
(tai)-[:PARENT_OF {order:3}]->(thu),
(tai)-[:PARENT_OF {order:4}]->(nhap),

(hai)-[:PARENT_OF {order:1}]->(kien),
(hai)-[:PARENT_OF {order:2}]->(quan),
(hai)-[:PARENT_OF {order:3}]->(duc),
(hai)-[:PARENT_OF {order:4}]->(nam1),
(hai)-[:PARENT_OF {order:5}]->(long1),

(ich)-[:PARENT_OF {order:1}]->(phung),
(phung)-[:PARENT_OF {order:1}]->(quang1),
(phung)-[:PARENT_OF {order:2}]->(anh1),
(phung)-[:PARENT_OF {order:3}]->(linh),

(hoan)-[:PARENT_OF {order:1}]->(khoan),
(hoan)-[:PARENT_OF {order:2}]->(vuon),

// MẬU branch
(mau)-[:PARENT_OF {order:1}]->(can),
(can)-[:PARENT_OF {order:1}]->(khai),

(khai)-[:PARENT_OF {order:1}]->(don),
(khai)-[:PARENT_OF {order:2}]->(luan),
(khai)-[:PARENT_OF {order:3}]->(thuy),

(don)-[:PARENT_OF {order:1}]->(kinh),
(don)-[:PARENT_OF {order:2}]->(tinh),
(don)-[:PARENT_OF {order:3}]->(hoan2),

(tinh)-[:PARENT_OF {order:1}]->(cuong),
(tinh)-[:PARENT_OF {order:2}]->(son),

(hoan2)-[:PARENT_OF {order:1}]->(hoang),

(luan)-[:PARENT_OF {order:1}]->(luu),
(luan)-[:PARENT_OF {order:2}]->(luyen),
(luan)-[:PARENT_OF {order:3}]->(lieu),
(luan)-[:PARENT_OF {order:4}]->(lien),
(luan)-[:PARENT_OF {order:5}]->(nam2),
(luan)-[:PARENT_OF {order:6}]->(vinh1),
(luan)-[:PARENT_OF {order:7}]->(huong),

(luyen)-[:PARENT_OF {order:1}]->(long2),
(luyen)-[:PARENT_OF {order:2}]->(thang),

(lieu)-[:PARENT_OF {order:1}]->(nam3),
(vinh1)-[:PARENT_OF {order:1}]->(quang2),

(huong)-[:PARENT_OF {order:1}]->(giang),
(huong)-[:PARENT_OF {order:2}]->(lam),

// TUẤN branch
(tuan)-[:PARENT_OF {order:1}]->(ca),
(ca)-[:PARENT_OF {order:1}]->(tung),
(tung)-[:PARENT_OF {order:1}]->(vu),

(vu)-[:PARENT_OF {order:1}]->(vinh2),
(vu)-[:PARENT_OF {order:2}]->(hung),

(vinh2)-[:PARENT_OF {order:1}]->(bao),
(vinh2)-[:PARENT_OF {order:2}]->(bang),

(hung)-[:PARENT_OF {order:1}]->(dung);
