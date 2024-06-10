from django.shortcuts import render, redirect
from .models import Trade
from .utils import get_plot
from .forms import LotForm
import datetime
from django.views.generic import ListView


class TradeListView(ListView):
    model = Trade
    template_name = 'trade/list.html'
    context_object_name = "trades"

    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Trade.objects.filter(user=self.request.user).order_by('-created_at')
        else:
            return Trade.objects.none()



def calculator(request):

    if request.method == 'POST':
        
        form = LotForm(request.POST)

        if form.is_valid():
            # amount = form.cleaned_data.get('amount')
            amount = request.POST.get('amount')
            amount = int(amount)
            loss_persentage = 0

            if amount <= 100:            #5
                loss_persentage += 5          
            elif 100 < amount <= 200:      #8
                loss_persentage += 4
            elif 200 < amount <= 430:      #13
                loss_persentage += 3
            elif 430 < amount <= 1050:     #21
                loss_persentage += 2
            elif 1050 < amount <= 3400:     #3400
                loss_persentage += 1
            elif 3400 < amount <= 6111:     #5500
                loss_persentage += 0.9
            elif 6111 < amount <= 11125:     #8900
                loss_persentage += 0.8
            elif 11125 < amount <= 20571:     #14400
                loss_persentage += 0.7
            elif 20571 < amount <= 38833:     #23300
                loss_persentage += 0.6
            elif 38833 < amount <= 75400:     #37700
                loss_persentage += 0.5
            elif 75400 < amount <= 152500:     #61000
                loss_persentage += 0.4
            elif 152500 < amount <= 329000:     #98700
                loss_persentage += 0.3
            elif 329000 < amount <= 798500:     #159700
                loss_persentage += 0.2
            elif 798500 < amount <= 2584000:     #258400
                loss_persentage += 0.1

            # loss_dollar = form.cleaned_data.get("loss_dollar")
            loss_dollar = request.POST.get('loss_dollar')

            loss_dollar = float(loss_dollar)

            loss_value = amount * (loss_persentage/100)
            loss_value = float(loss_value)
            lot = loss_value / loss_dollar
            lot = round(lot,2)
        return render(request, "trade/calculator.html", context={'lot' : lot})
        
    else:
        form = LotForm()
        return render(request, "trade/calculator.html")
    


    

def statistic(request):

    user = request.user
    # جمع آوری اطلاعات مورد نیاز برای نمودار
    total = []
    days = []
    for trade in Trade.objects.all().filter(user=user):
        if trade.result == "Success":
            money = trade.total_money + trade.profit_or_loss
        else:
            money = trade.total_money - trade.profit_or_loss
        total.append(money)
        day = trade.created_at
        days.append(day)

    chart = get_plot(days, total)
    context = {'chart' : chart}

    return render(request, "trade/statistic.html", context)


def create_trade(request):

    user = request.user

    if request.method == "POST":

        lot = request.POST.get('lot')
        total_money = request.POST.get('total_money')
        profit_or_loss = request.POST.get('profit_or_loss')
        result = request.POST.get('result')
        day = request.POST.get('day')

        trade = Trade.objects.create(
            lot=lot,
            total_money=total_money,
            profit_or_loss=profit_or_loss,
            result=result,
            day=day,
            user=user
        )
        trade.save()
        # messages.success(request, "Trade Added!")
        return redirect('all-trade')
    return render(request, 'trade/create.html')


def trade_report(request):

    user = request.user

    if len(Trade.objects.all().filter(user=user)) == 0:
        context = {
            'primary_money':0,
            'total_money' : 0,
            'percent_growth' : 0,
            'profit' : 0,
            'total_trades' : 0,
            'winrate': 0,
            'win_trades' : 0,
            'lose_trades' : 0,
            'weekly_trades': 0,
            'monthly_trades': 0,
            'quarterly_trades': 0,
        }
        return render(request, 'trade/trade_report.html', context=context)

    today = datetime.date.today()

    #فیلتر کردن تریدها بر اساس بازه‌های زمانی
    weekly_trades = Trade.objects.filter(created_at__gte=today - datetime.timedelta(days=7))
    monthly_trades = Trade.objects.filter(created_at__gte=today - datetime.timedelta(days=30))
    quarterly_trades = Trade.objects.filter(created_at__gte=today - datetime.timedelta(days=90))

    total_trades = Trade.objects.all().filter(user=user)
    first_trade = total_trades.first()
    last_trade = total_trades.last()
    primary_money = first_trade.total_money

    if last_trade.result == "Success":
        total_money = last_trade.total_money + last_trade.profit_or_loss
    else:
        total_money = last_trade.total_money - last_trade.profit_or_loss

    percent_growth = (total_money-primary_money) / primary_money * 100

    profit = total_money - primary_money
    
    profit=round(profit,1)
    percent_growth=round(percent_growth,1)

    lose_trades = Trade.objects.all().filter(user=user, result="Failed")

    win_trades = Trade.objects.all().filter(user=user, result="Success")

    winrate = len(win_trades) / len(total_trades) * 100

    winrate = round(winrate, 2)

    context = {
        'primary_money':primary_money,
        'total_money' : total_money,
        'percent_growth' : percent_growth,
        'profit' : profit,
        'total_trades' : len(total_trades),
        'winrate': winrate,
        'win_trades' : len(win_trades),
        'lose_trades' : len(lose_trades),
        'weekly_trades': weekly_trades,
        'monthly_trades': monthly_trades,
        'quarterly_trades': quarterly_trades,
    }

    return render(request, 'trade/trade_report.html', context=context)