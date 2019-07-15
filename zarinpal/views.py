from django.http import HttpResponse
from django.shortcuts import redirect
from cart.views import get_total_price, clear_cart
from zeep import Client


MERCHANT = '11111111-1111-1111-1111-111111111111'

client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')

# Toman / Required
#amount = 5000


description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required

email = 'Lordofhell225@gmail.com'  # Optional

mobile = '09123456789'  # Optional

# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/verify/'


def send_request(request):
    amount = get_total_price(request)
    result = client.service.PaymentRequest(
        MERCHANT, amount, description, email, mobile, CallbackURL)

    if result.Status == 100:

        return redirect('https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority))

    else:

        return HttpResponse('Error code: ' + str(result.Status))


def verify(request):
    amount = get_total_price(request)

    if request.GET.get('Status') == 'OK':

        result = client.service.PaymentVerification(
            MERCHANT, request.GET['Authority'], amount)

        if result.Status == 100:
            clear_cart(request)
            return redirect('pages:home-page')
            # return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))

        elif result.Status == 101:

            return redirect('cart:cart')
            # return HttpResponse('Transaction submitted : ' + str(result.Status))

        else:

            return redirect('cart:cart')
            # return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))

    else:

        return redirect('cart:cart')
        # return HttpResponse('Transaction failed or canceled by user')
