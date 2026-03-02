import re
import json

def clean_num(s):
    return float(s.replace('\u202f', '').replace('\xa0', '').replace(' ', '').replace(',', '.'))

def parse_receipt(filepath):
    text = open(filepath, encoding='utf-8').read()
    lines = text.split('\n')

    # Store info
    store_info = {
        "name": re.search(r'Филиал .+', text).group(0).strip(),
        "bin": re.search(r'БИН\s+(\d+)', text).group(1),
        "receipt_number": re.search(r'Чек №(\d+)', text).group(1),
        "cashier": re.search(r'Кассир\s+(.+)', text).group(1).strip(),
    }

    # Date/time
    dt = re.search(r'Время:\s+(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})', text)
    datetime_info = {"date": dt.group(1), "time": dt.group(2), "full": f"{dt.group(1)} {dt.group(2)}"}

    # Payment
    payment_method = "Банковская карта" if "Банковская карта" in text else "Наличные"
    pay_m = re.search(r'Банковская карта:\s*([\d\xa0\s]+,\d{2})', text)
    payment_amount = clean_num(pay_m.group(1)) if pay_m else None

    # Items
    QP = re.compile(r'^([\d\xa0\s]+,\d+)\s+x\s+([\d\xa0\s]+,\d+)$')
    ID = re.compile(r'^(\d+)\.$')

    items = []
    i = 0
    while i < len(lines):
        m = ID.match(lines[i].strip())
        if m:
            idx = int(m.group(1))
            i += 1
            name_lines = []
            while i < len(lines) and not QP.match(lines[i].strip()):
                if lines[i].strip():
                    name_lines.append(lines[i].strip())
                i += 1
            name = ' '.join(name_lines).strip()
            qp = QP.match(lines[i].strip())
            qty = clean_num(qp.group(1))
            unit_price = clean_num(qp.group(2))
            i += 1
            items.append({
                "index": idx,
                "name": name,
                "quantity": qty,
                "unit_price": unit_price,
                "total": round(qty * unit_price, 2)
            })
        else:
            i += 1

    # Totals
    total_m = re.search(r'ИТОГО:\s*([\d\xa0\s]+,\d{2})', text)
    grand_total = clean_num(total_m.group(1)) if total_m else sum(it['total'] for it in items)
    vat_m = re.search(r'НДС 12%:\s*([\d\xa0\s]+,\d{2})', text)
    vat = clean_num(vat_m.group(1)) if vat_m else 0.0

    # Fiscal
    fs = re.search(r'Фискальный признак:\s*(\d+)', text)
    kkm = re.search(r'Код ККМ КГД \(РНМ\):\s*(\d+)', text)
    znm = re.search(r'ЗНМ:\s*(\S+)', text)

    return {
        "store_info": store_info,
        "datetime": datetime_info,
        "items": items,
        "summary": {
            "item_count": len(items),
            "calculated_total": round(sum(it['total'] for it in items), 2),
            "receipt_total": grand_total,
            "vat_12_percent": vat,
            "payment_method": payment_method,
            "payment_amount": payment_amount,
        },
        "fiscal": {
            "fiscal_sign": fs.group(1) if fs else None,
            "kkm_code": kkm.group(1) if kkm else None,
            "znm": znm.group(1) if znm else None,
        }
    }

if __name__ == "__main__":
    data = parse_receipt("raw.txt")

    # Print report
    print(f"Store   : {data['store_info']['name']}")
    print(f"Receipt : #{data['store_info']['receipt_number']}")
    print(f"Date    : {data['datetime']['full']}\n")
    print(f"{'#':<4} {'Product':<46} {'Qty':>5} {'Price':>10} {'Total':>10}")
    print("-" * 75)
    for it in data["items"]:
        print(f"{it['index']:<4} {it['name'][:45]:<46} {it['quantity']:>5.0f} {it['unit_price']:>10.2f} {it['total']:>10.2f}")
    s = data["summary"]
    print("-" * 75)
    print(f"{'TOTAL':<55} {s['receipt_total']:>10.2f} KZT")
    print(f"Payment : {s['payment_method']} — {s['payment_amount']:.2f} KZT")
    print(f"VAT 12% : {s['vat_12_percent']:.2f} KZT")

    # Save JSON
    with open("parsed_receipt.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("\nSaved: parsed_receipt.json")
