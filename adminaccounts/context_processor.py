from orders.models import Order,OrderItem



def revenue_calculator(request):

    revenue = 0

    tax = 0

    total_revenue = 0

    try:

        orders = Order.objects.all()

        for order in orders:

            tax += order.payment.tax
            
        order_items = OrderItem.objects.all()

        for item in order_items:

            if item.order_status == 'Delivered':

                revenue += item.item_total
        
        total_revenue = revenue + tax

        return dict(revenue=total_revenue)
    
    except OrderItem.DoesNotExist:

        pass