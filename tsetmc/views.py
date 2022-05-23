import numbers
import traceback

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import math


# Create your views here.
@csrf_exempt
def api(request):
    # محاسبه نسبت

    import time
    import pandas as pd
    import finpy_tse as tse
    # import jdatetime
    import openpyxl
    import string
    import os
    # import xlwt
    import shutil

    def n2a(n, b=string.ascii_uppercase):
        d, m = divmod(n, len(b))
        return n2a(d - 1, b) + b[m] if d else b[m]

    def isfloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    # writepath = r'coef.xlsx'
    # if not os.path.exists(writepath):
    #     print(f'The file ({path_to_file}) does not exist')
    #     # original = r'C:/Users/mk/Desktop/ModaberAsia/back up 11/excel/Fund.xlsx'
    #     target2 = f'{target}coef.xlsx'
    #     shutil.copyfile(original, target2)
    #     print("file  created")

    writepath = r'coef.xlsx'
    if not os.path.exists(writepath):
        original = r'./template.xlsx'
        # target2 = f'{target}coef.xlsx'
        shutil.copyfile(original, writepath)
        print("file  created")

    def multple(ta):
        ta = int(ta)
        erorta = 0

        while True:
            try:
                DF5 = tse.Get_MarketWatch(save_excel=False)
                break
            except Exception as e:
                erorta += 1
                print(
                    e, "\n", erorta, '**internet connection error , please check your internet or turn off your vpn**')
                time.sleep(10)

        li = pd.DataFrame(list(DF5)[0])
        li2 = pd.DataFrame(list(DF5)[1])

        namad = pd.DataFrame(pd.DataFrame(
            li2.index.tolist()).loc[:, 0]).drop_duplicates()
        namad = namad.reset_index().drop(columns=['index'])
        namad
        dict1 = {}

        while True:
            try:
                listfilewb = "coef.xlsx"
                wbkName = listfilewb
                print("Excel location: ", wbkName)
                wbk = openpyxl.load_workbook(wbkName)
                wks = wbk['Sheet1']
                wks["A" + str(1)].value = "نماد"
                wks["B" + str(1)].value = "Buy/Sell"
                wks["C" + str(1)].value = "R AND L"

                wks[n2a(ta + 1) + str(1)].value = time.strftime("%H:%M:%S")
                for j in range(len(namad)):
                    try:

                        Buy_Price = li2.loc[namad.values[j]
                        [0]]['Buy-Price'].tolist()
                        Sell_Price = li2.loc[namad.values[j]
                        [0]]['Sell-Price'].tolist()

                        # if Buy_Price == li.loc[namad.values[j][0]].iloc[10]:
                        #     pass
                        Buy_Vol = li2.loc[namad.values[j][0]]['Buy-Vol'].tolist()
                        Sell_Vol = li2.loc[namad.values[j][0]]['Sell-Vol'].tolist()

                        high = li.loc[namad.values[j][0]].iloc[9]
                        low = li.loc[namad.values[j][0]].iloc[10]
                        Vol_Buy_I = li.loc[namad.values[j][0]].iloc[18]
                        Vol_Sell_I = li.loc[namad.values[j][0]].iloc[20]
                        Close = li.loc[namad.values[j][0]].iloc[5]

                        popbuylist = []
                        popselllist = []

                        for xx, x in enumerate(Buy_Price):
                            if x > high and x != 0:
                                popbuylist.append(xx)
                                # print("Buy_Pricehigh", namad.values[j][0], xx, x)
                                # Buy_Price.pop(i)
                                # Buy_Vol.pop(i)
                            if x < low and x != 0:
                                # print("Buy_Pricelow", namad.values[j][0], xx, x)
                                popbuylist.append(xx)
                                # Buy_Price.pop(i)
                                # Buy_Vol.pop(i)

                        for yy, y in enumerate(Sell_Price):
                            if y > high and y != 0:
                                # print("Sell_Pricehigh", namad.values[j][0], yy, y)
                                popselllist.append(yy)
                                # Sell_Price.pop(u)
                                # Sell_Vol.pop(u)
                            if y < low and y != 0:
                                # print("Sell_Pricelow", namad.values[j][0], yy, y)
                                popselllist.append(yy)
                                # Sell_Price.pop(u)
                                # Sell_Vol.pop(u)

                        # # for aa, a in enumerate(Buy_Price):
                        # for k in popbuylist:
                        #     print("oldBuy_Price",Buy_Price)
                        #     print("popbuylist",k)
                        #     Buy_Price.pop(k)
                        #     Buy_Vol.pop(k)
                        #     print("okpopbuylist",k)
                        #     print("newBuy_Price",Buy_Price)

                        # # for bb, b in enumerate(Sell_Price):
                        # for g in popselllist:
                        #     print("oldSell_Price",Sell_Price)
                        #     print("popselllist",g)

                        #     Sell_Price.pop(g)
                        #     Sell_Vol.pop(g)
                        #     print("okpopbuylist",g)
                        #     print("oldSell_Price",Sell_Price)

                        Buy_Price = [iii for jjj, iii in enumerate(Buy_Price) if jjj not in popbuylist]
                        Buy_Vol = [iii for jjj, iii in enumerate(Buy_Vol) if jjj not in popbuylist]

                        Sell_Price = [iii for jjj, iii in enumerate(Sell_Price) if jjj not in popselllist]
                        Sell_Vol = [iii for jjj, iii in enumerate(Sell_Vol) if jjj not in popselllist]

                        multiply_Buy = [Buy_Price[i] * Buy_Vol[i]
                                        for i in range(len(Buy_Price))]
                        multiply_Sel = [Sell_Price[i] * Sell_Vol[i]
                                        for i in range(len(Sell_Vol))]
                        Sum_Buy = sum(multiply_Buy)
                        Sum_Sel = sum(multiply_Sel)

                        power = (Vol_Sell_I - Vol_Buy_I) * Close

                        if isfloat(str(power)):
                            power = float(str(power))
                        else:
                            power = 0

                        if math.isnan(power):
                            # print("power", power)
                            power = 0

                        # print(power)

                        try:
                            dict1[namad.values[j][0]] = {"id": j,
                                                         "name": namad.values[j][0],
                                                         "power": power,
                                                         "coef": int(Sum_Buy) / \
                                                                 int(Sum_Sel),
                                                         "time": time.strftime("%H:%M:%S"),
                                                         }
                            wks["A" + str(j + 2)].value = namad.values[j][0]
                            wks["C" + str(j + 2)].value = (Vol_Sell_I - Vol_Buy_I) * Close
                            wks[n2a(ta + 2) + str(j + 2)].value = int(Sum_Buy) / \
                                                                  int(Sum_Sel)
                        except ZeroDivisionError:
                            dict1[namad.values[j][0]] = {"id": j,
                                                         "name": namad.values[j][0],
                                                         "power": power,
                                                         "coef": -1,
                                                         "time": time.strftime("%H:%M:%S"),
                                                         }

                            wks["A" + str(j + 2)].value = namad.values[j][0]
                            wks["C" + str(j + 2)].value = (Vol_Sell_I - Vol_Buy_I) * Close
                            wks[n2a(ta + 2) + str(j + 2)].value = -1


                    except Exception as e:
                        print(namad.values[j][0])
                        print(traceback.format_exc())
                        # print(e)
                        wks["A" + str(j + 2)].value = namad.values[j][0]
                        wks[n2a(ta + 2) + str(j + 2)].value = -2

                wbk.save(wbkName)
                print("Write Successfully")
                break
            except Exception as e:
                print(e)
                # print(traceback.format_exc())
                print("\n--------------------------------")
                print(
                    "'fit.xlsx' is open OR excel file is crashed \nplease close 'fit.xlsx' to see update")
                print("--------------------------------\n")
                time.sleep(3)

        return dict1

    ta = 0
    # while True:
    ta += 1
    print("Time:" + str(time.strftime("%H:%M:%S")), "  Tedad:", ta)
    start = time.time()
    dict1 = multple(ta)
    end = time.time()
    print("Run Time: ", end - start)
    # time.sleep(15)

    return JsonResponse(dict1, safe=False)


@csrf_exempt
def home(request):
    return render(request, 'home.html')


@csrf_exempt
def api2(request):
    return JsonResponse({"aa": "ee"}, safe=False)


def home1(request):
    return render(request, 'home1.html')
