# -*- coding: utf-8 -*-
# @Author: mb-zaba
# @Date:   2021-02-20 11:00:01
# @Last Modified by:   mb-zaba
# @Last Modified time: 2021-02-20 11:05:44

from krakenpy import krakenpy

k = krakenpy()
print(k.get_order_book('ETHEUR'))
