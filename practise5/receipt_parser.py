import re

s = open("raw.txt", encoding="utf-8").read()
Money = r"\d[\d ]*,\d{2}"
to_float = lambda s: float(s.replace(" ", "").replace(",", "."))
datetime = re.search(r"\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2}", s)
pay = re.search("Банковская карта|Наличные", s, re.I)

items = []
pattern = f"(?ms)^\d+\.\n(.*?)\n\d+,\d{{3}} x {Money}\n({Money})"

for i in re.finditer(pattern, s):
    items.append({"название": i.group(1), "цена": to_float(i.group(2))})
sum = sum(n["цена"] for n in items)

print("Дата/время:", datetime.group(0))
print("Способ оплаты:", pay.group(0))
print("Количество товаров:", len(items))
print("Итоговая сумма:", sum)
print("\nТовары:")

i = 1
for j in items:
    print(f"{i} - {j['название']} — {j['цена']}")
    i +=1