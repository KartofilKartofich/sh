import streamlit as st
import numpy as np
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
from streamlit_server_state import server_state as ss
import urllib
from datetime import datetime, timedelta
import math
#from streamlit_carousel import carousel
from streamlit_image_select import image_select
import random
from pathlib import Path
import base64
import io
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.affinity import scale


st.markdown("""
<style>
    * {
       overflow-anchor: none !important;
       }
</style>""", unsafe_allow_html=True)

# st.markdown("""
# <style>
#     *, ::before, ::after {
#     box-sizing: inherit;
#     }
# </style>""", unsafe_allow_html=True)
def enc(s):

    if not s:
        return ""
    
    result = []
    
    for i, char in enumerate(s):
        result.append(char)
        
        if char.isalpha():
            random_letter = random.choice(st.secrets['letters'])
            result.append(random_letter)
        
        elif char.isdigit():
            random_digit = random.choice('0123456789')
            result.append(random_digit)
    
    return ''.join(result)

# ----------------------------------N_MAPS---------------------------------------------
STREETS = st.secrets['STREETS']
CITIES = st.secrets['CITIES']
COUNTRIES = st.secrets['COUNTRIES']
PLACES = st.secrets['PLACES']
POST_SERVICES = st.secrets['POST_SERVICES']

ph = st.empty()

if "value" not in st.session_state:
    st.session_state["value"] = {}

if "country" not in st.session_state:
    st.session_state["country"] = ""
    st.session_state["city"] = ""
    st.session_state["street"] = ""
    st.session_state["extra"] = ""
    st.session_state["floor"] = ""
    st.session_state["ind"] = None

polygon_outer = Polygon(st.secrets["polygon_outer"])
polygon_inner = Polygon(st.secrets["polygon_inner"])

pts_e_3 = Polygon(st.secrets["pts_e_3"])
pts_e_4 = Polygon(st.secrets["pts_e_4"])
pts_e_5 = Polygon(st.secrets["pts_e_5"])
pts_e_6 = Polygon(st.secrets["pts_e_6"])

pts_1 = Polygon(st.secrets["pts_1"])
pts_2 = Polygon(st.secrets["pts_2"])
pts_4 = Polygon(st.secrets["pts_4"])
pts_5 = Polygon(st.secrets["pts_5"])
pts_6 = Polygon(st.secrets["pts_6"])
pts_7 = Polygon(st.secrets["pts_7"])
pts_8 = Polygon(st.secrets["pts_8"])
pts_11 = Polygon(st.secrets["pts_11"])


pts_31 = Polygon(st.secrets["pts_31"])
pts_32 = Polygon(st.secrets["pts_32"])
pts_33 = Polygon(st.secrets["pts_33"])
pts_34 = Polygon(st.secrets["pts_34"])
pts_35 = Polygon(st.secrets["pts_35"])
pts_36 = Polygon(st.secrets["pts_36"])
pts_37 = Polygon(st.secrets["pts_37"])
pts_38 = Polygon(st.secrets["pts_38"])
pts_39 = Polygon(st.secrets["pts_39"])

pts_41 = Polygon(st.secrets["pts_41"])
pts_42 = Polygon(st.secrets["pts_42"])
pts_43 = Polygon(st.secrets["pts_43"])
pts_44 = Polygon(st.secrets["pts_44"])
pts_45 = Polygon(st.secrets["pts_45"])
pts_46 = Polygon(st.secrets["pts_46"])

pts_51 = Polygon(st.secrets["pts_51"])
pts_52 = Polygon(st.secrets["pts_52"])
pts_53 = Polygon(st.secrets["pts_53"])
pts_54 = Polygon(st.secrets["pts_54"])
pts_55 = Polygon(st.secrets["pts_55"])

pts_61 = Polygon(st.secrets["pts_61"])

pts_81 = Polygon(st.secrets["pts_81"])
pts_82 = Polygon(st.secrets["pts_82"])
pts_83 = Polygon(st.secrets["pts_83"])
pts_84 = Polygon(st.secrets["pts_84"])

circle = Point(st.secrets["circle"][0], st.secrets["circle"][1]).buffer(st.secrets["circle"][2])

circle_1 = Point(st.secrets["circle_1"][0], st.secrets["circle_1"][1]).buffer(st.secrets["circle_1"][2]) # Start with a unit circle centered at (0,0)
#ellipse = scale(circle_1, xfact=5, yfact=10) # Scale it to desired dimensions
# Translate the ellipse to its desired center (e.g., (10, 10))
ellipse = scale(circle_1, xfact=st.secrets["ellipse"][2], yfact=st.secrets["ellipse"][3], origin=(st.secrets["ellipse"][0],st.secrets["ellipse"][1])) 

st_dict = {STREETS[3]:0,
                STREETS[0]:1,
                STREETS[6]:2,
                STREETS[4]:3,
                STREETS[5]:4,
                STREETS[8]:5,
                STREETS[2]:6,
                STREETS[7]:7,
                STREETS[9]:8,
                STREETS[1]:9,
                "":10}
st_l = [STREETS[3],
                STREETS[0],
                STREETS[6],
                STREETS[4],
                STREETS[5],
                STREETS[8],
                STREETS[2],
                STREETS[7],
                STREETS[9],
                STREETS[1],
                ""]

def addr():
    st.session_state["country"] = ""
    st.session_state["city"] = ""
    st.session_state["street"] = ""
    st.session_state["extra"] = ""
    st.session_state["floor"] = ""
#value
    map_image_name = "map_4_with_logo"
    giant_str_map = st.secrets["pics"][map_image_name] 
    im_map = Image.open(io.BytesIO(base64.decodebytes(bytes(giant_str_map, "utf-8"))))

    st.session_state["value"] = streamlit_image_coordinates(im_map,height=480, width=640,
                                    use_column_width="never",
                                    cursor="crosshair")#'always')
    #st.write(st.session_state["value"])

    # a = 640
    # if value:
    #     x, y = 2*value["x"], 2*value["y"]
    if st.session_state["value"]:
        x, y = 2*st.session_state["value"]["x"], 2*st.session_state["value"]["y"]
        st.write(x,y)

        point = Point(x, y)
        #st.write(polygon.contains(point))

        #if x < a / 2 and y < a / 2:
        if not polygon_outer.contains(point):
            st.session_state["country"] = COUNTRIES[1]
            st.session_state["city"] = CITIES[0]
            st.session_state["street"] = ""
        elif not polygon_inner.contains(point):
            if pts_e_5.contains(point):
                st.session_state["country"] = COUNTRIES[0]
                st.session_state["street"] = STREETS[5]
                st.session_state["extra"] = PLACES["pts_e_5"]
            elif pts_e_4.contains(point):
                st.session_state["country"] = COUNTRIES[0]
                st.session_state["street"] = STREETS[4]
                st.session_state["extra"] = PLACES["pts_e_4"]
            elif pts_e_3.contains(point):
                st.session_state["country"] = COUNTRIES[0]
                st.session_state["street"] = STREETS[6]
            elif pts_e_6.contains(point):
                st.session_state["country"] = COUNTRIES[1]
                st.session_state["city"] = CITIES[0]
                st.session_state["street"] = ""
            elif pts_45.contains(point):
                st.session_state["country"] = COUNTRIES[0]
                st.session_state["street"] = STREETS[4]
                st.session_state["extra"] = PLACES["pts_45"]
            else:
                st.toast("🚨 Вы ткнули в стену")
        #     street = "Улица Marx"
        # elif x < a / 2 and y >= a / 2:
        #     street = "Улица Калинина"
        else:
            if pts_5.contains(point):
                st.session_state["country"] = COUNTRIES[2]
                st.session_state["street"] = ""
                st.session_state["extra"] = ""

            else:
                st.session_state["country"] = COUNTRIES[0]
                st.session_state["extra"] = ""

                if pts_7.contains(point):
                    st.session_state["street"] = STREETS[4]

                    if pts_e_4.contains(point):
                        st.session_state["extra"] = PLACES["pts_e_4"]
                    else:
                        if pts_41.contains(point):
                            st.session_state["extra"] = PLACES["pts_41"]
                        elif pts_42.contains(point):
                            st.session_state["extra"] = PLACES["pts_42"]
                        elif pts_43.contains(point):
                            st.session_state["extra"] = PLACES["pts_43"]
                        elif pts_44.contains(point):
                            st.session_state["extra"] = PLACES["pts_44"]
                        elif pts_46.contains(point):
                            st.session_state["extra"] = PLACES["pts_46"]
                    

                elif pts_8.contains(point):
                    st.session_state["street"] = STREETS[8]

                    if pts_11.contains(point):
                        st.session_state["extra"] = PLACES["pts_11"]
                    elif pts_61.contains(point):
                        st.session_state["extra"] = PLACES["pts_61"]

                elif pts_4.contains(point):
                    st.session_state["street"] = STREETS[5]
                    
                    if pts_e_5.contains(point):
                        st.session_state["extra"] = PLACES["pts_e_5"]
                    else:
                        if pts_51.contains(point):
                            st.session_state["extra"] = PLACES["pts_51"]
                        elif pts_52.contains(point):
                            st.session_state["extra"] = PLACES["pts_52"]
                        elif pts_53.contains(point):
                            st.session_state["extra"] = PLACES["pts_53"]
                        elif pts_54.contains(point):
                            st.session_state["extra"] = PLACES["pts_54"]
                        elif pts_55.contains(point):
                            st.session_state["extra"] = PLACES["pts_55"]
                    

                elif pts_2.contains(point):
                    st.session_state["street"] = STREETS[2]

                    if pts_82.contains(point):
                        st.session_state["extra"] = PLACES["pts_82"]
                    elif pts_83.contains(point):
                        st.session_state["extra"] = PLACES["pts_83"]
                    elif pts_84.contains(point):
                        st.session_state["extra"] = PLACES["pts_84"]
                
                elif pts_1.contains(point):
                    st.session_state["street"] = STREETS[1]

                    if not pts_81.contains(point):
                        st.session_state["extra"] = PLACES["pts_81"]
                    else:
                        if ellipse.contains(point):
                            st.session_state["extra"] = PLACES["ellipse"]      

                elif pts_6.contains(point):
                    if not pts_e_3.contains(point):
                        if y <= 189 + 14 + 99 * 2 :
                            st.session_state["street"] = STREETS[3]
                            if pts_35.contains(point):
                                st.session_state["extra"] = PLACES["pts_35"]
                            elif pts_34.contains(point):
                                st.session_state["extra"] = PLACES["pts_34"]
                            elif pts_33.contains(point):
                                st.session_state["extra"] = PLACES["pts_33"]  
                            elif pts_32.contains(point):
                                st.session_state["extra"] = PLACES["pts_32"]
                            elif pts_38.contains(point):
                                st.session_state["extra"] = PLACES["pts_38"]
                            elif pts_39.contains(point):
                                st.session_state["extra"] = PLACES["pts_39"]
                        else:
                            #st.session_state["street"] = STREETS[0] or "ББ"
                            if pts_36.contains(point):
                                st.session_state["extra"] = PLACES["pts_36"]
                            else:
                                st.session_state["street"] = STREETS[0]
                                if pts_31.contains(point):
                                    st.session_state["extra"] = PLACES["pts_31"]
                                elif pts_32.contains(point):
                                    st.session_state["extra"] = PLACES["pts_32"]
                                elif pts_37.contains(point):
                                    st.session_state["extra"] = PLACES["pts_37"]     
                                elif circle.contains(point):
                                    st.session_state["extra"] = PLACES["circle"]      
                                # @st.dialog("floor_selection")
                                # def select_floor():
                                #     st.session_state["floor"] = st.selectbox("Выберите этаж", 
                                            
                                #             options=["1","2","3","4","5","6","крыша"], 
                                #             #on_change=addr()#exception_street_callback()
                                #             )
                                    

                                #     if st.session_state["floor"]=="5":
                                #         st.session_state["street"] = STREETS[7]
                                #     else: 
                                #         st.session_state["street"] = STREETS[0]

                                # select_floor()
                                # else:
                                #     st.session_state["street"] = STREETS[0]
                    else:
                        st.session_state["street"] = STREETS[6]
                else:
                    st.toast("🚨 Вы ткнули в стену. Попробуйте ещё раз")
            #address_1 =  country
    else:
        #address_1 = ""
        pass
# ----------------------------------N_MAPS---------------------------------------------

RATES = st.secrets['rates']
CLEANUP_TIME = st.secrets['CLEANUP_TIME_IN_MINUTES']

def s_1(data: bytes, s: int) -> bytes:
    s = st.secrets['s']
    random.seed(s)
    return bytes(b ^ random.randint(0, 255) for b in data)

@st.cache_data
def l_1(p1: str, p2: str):
    
    s = st.secrets['s']
    l = st.secrets["ps"][p1]
    r = Path("i/"+p2).read_text(encoding='utf-8')
    f = l + r
    i = base64.b64decode(f)
    i = s_1(i, s)

    return i

def convert_currency2(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount
    amount_in_target = amount * RATES[to_currency] / RATES[from_currency] 
   
    return math.ceil(amount_in_target*100)/100

# ------------------------------------------------------------------
# 1. Загрузка товаров из secrets.toml
# ------------------------------------------------------------------
products = st.secrets["products"]  # список словарей
promos = st.secrets["promos"]
#st.write(products)

# ------------------------------------------------------------------
# 2. Глобальные состояния (запасы, резерв мест, пользователи, доступные user_id)
# ------------------------------------------------------------------
if "stock" not in ss:
    ss.stock = {}
    for p in products:
        pid = str(p["id"])
        if "stock" in p:  # обычный товар
            ss.stock[pid] = p["stock"]
        elif p["category"] == "Книги":  # книга
            ss.stock[f"{pid}_paper"] = p.get("stock_paper", 0)
            ss.stock[f"{pid}_e"] = p.get("stock_e", 0)
        elif p["category"] == "Аудиокниги":  # книга
            ss.stock[f"{pid}_opta"] = p.get("stock_opta", 0)
            ss.stock[f"{pid}_optb"] = p.get("stock_optb", 0)

if "seats" not in ss:
    ss.seats = {}  # {time_str: {"1-1": True/False, ...}}

if "users" not in ss:
    ss.users = {}  # {user_id: {"cart": {pid: qty}, "login_time": datetime}}

if "available_user_ids" not in ss:
    # Инициализация списка доступных user_id (100-999, первая цифра не 0)
    ss.available_user_ids = list(range(100, 1000))
    np.random.shuffle(ss.available_user_ids)  # Перемешиваем для случайности

if "no_more_cart_cleaning" not in st.session_state:
    st.session_state.no_more_cart_cleaning = False
if "no_more_stock_updating" not in st.session_state:
    st.session_state.no_more_stock_updating = False

# ------------------------------------------------------------------
# 3. Конфигурация страницы
# ------------------------------------------------------------------
st.set_page_config(page_title="Магазин", page_icon="🛒", layout="centered")

# ------------------------------------------------------------------
# 4. Фильтры (категория / страна / бренд)
# ------------------------------------------------------------------
categories = ["Все"] + sorted({p["category"] for p in products})
countries = ["Все"] + sorted({p["country"] for p in products})
brands = ["Все"] + sorted({p["brand"] for p in products})

# ------------------------------------------------------------------
# 5. session_state (user_id, показ адреса, выбор валюты для первой корзины)
# ------------------------------------------------------------------
def assign_unique_user_id():
    """Присваивает уникальный трёхзначный user_id пользователю."""
    if not ss.available_user_ids:
        st.error("Достигнуто максимальное количество пользователей. Пожалуйста, попробуйте позже.")
        st.stop()
    user_id = ss.available_user_ids.pop()
    return str(user_id)


# ------------------------------------------------------------------
dev_mode = st.query_params.get("dev_mode", "")
if dev_mode == st.secrets["DEV_MODE"]:
   dev_mode = 1
else:
   dev_mode = 0

if dev_mode == 1:
   cart_upd_str = st.query_params.get("cart_upd", "")

   if st.session_state.no_more_stock_updating == False and cart_upd_str != "":
        for item in cart_upd_str.split(";"):
            if not item:
                continue
            p_id,delta_qty = item.split(",")
            if p_id in ss.stock:
                ss.stock[p_id] = ss.stock.get(p_id, 0) + int(delta_qty) # delta > 0 или delta < 0
                st.write(f"Обновили кол-во товара {p_id} на {delta_qty}")
        st.session_state.no_more_stock_updating = True

   

if "user_id" not in st.session_state:
    u_id = st.query_params.get("id", "")

    if u_id == "": #если не задан в query
        st.session_state.user_id = assign_unique_user_id()
    else:
        st.session_state.user_id = str(u_id)

# user_id = st.session_state.user_id

# Инициализация данных пользователя, если его ещё нет
if st.session_state.user_id not in ss.users:
    # st.write("initialization")
    ss.users[st.session_state.user_id] = {
        "cart": {str(p["id"]): 0 for p in products},
        "login_time": datetime.utcnow()
    }
    for p in products:
        if p["category"] == "Книги":
            ss.users[st.session_state.user_id]["cart"][f"{p['id']}_paper"] = 0
            ss.users[st.session_state.user_id]["cart"][f"{p['id']}_e"] = 0
        if p["category"] == "Аудиокниги":
            ss.users[st.session_state.user_id]["cart"][f"{p['id']}_opta"] = 0
            ss.users[st.session_state.user_id]["cart"][f"{p['id']}_optb"] = 0

if "show_address" not in st.session_state:
    st.session_state.show_address = False

if "preferred_cur" not in st.session_state:
    st.session_state.preferred_cur = f'UNI, {st.secrets.cur["UNI"]["forms"][4]}'#"UNI"

logo_name = st.secrets['logo_name']

im_bytes = l_1(logo_name, f"{logo_name}.txt")

st.image(im_bytes, 
         #width=50
         )


#Показывать цены в
every_cur = [f'{i}, {st.secrets.cur[i]["forms"][4]}' for i in RATES.keys()]
#every_cur = [i for i in RATES.keys()]

_, col2 = st.columns([0.7, 0.3])

with col2:
    st.session_state.preferred_cur = st.selectbox(
                        "Показывать международные цены в валюте :",
                        every_cur,
                    )

# ------------------------------------------------------------------
# 7. Вспомогательная функция – «цветное» изображение
# ------------------------------------------------------------------
def generate_image(color, size=150):
    arr = np.zeros((size, size, 3), dtype=np.uint8)
    arr[:, :] = color
    return Image.fromarray(arr)

# ------------------------------------------------------------------
# 8. UI – две вкладки
# ------------------------------------------------------------------
tab_products, tab_cart, tab_hello = st.tabs(
    ["🛍 Товары", "🛒 Корзина", "Информация"]
)

# ------------------------------------------------------------------
# 9. Callback для кнопки «Купить»
# -----------------------------------------------
def buy_callback(pid: str, vtype: str = None):
    # Получение ключа товара
    key = pid if vtype is None else f"{pid}_{vtype}"
    avail = ss.stock.get(key, 0)
    
    if avail == 0.5:
        ss.stock[key] = 0
        st.toast("🤫 *распродали только что прямо перед вами*")
        return
    
    if avail <= 0:
        st.toast("🤫 *распродали только что прямо перед вами*")
        return
    
    prod = next(p for p in products if str(p["id"])==pid)
    max_items_per_one_order = prod['max_items']

    user_cart = ss.users[st.session_state.user_id]["cart"]
    if user_cart.get(key, 0) < max_items_per_one_order:

        # Обновление запаса
        ss.stock[key] = max(0, avail - 1)
        
        # Обновление корзины пользователя
        #user_cart = ss.users[st.session_state.user_id]["cart"]
        user_cart[key] = user_cart.get(key, 0) + 1

        st.toast("Товар добавлен в корзину!")
    else:
        st.toast(f"🤫 *в одном заказе может быть не более {max_items_per_one_order} таких товаров*")
    
    # Обновление времени входа (для предотвращения повторной очистки)
    ss.users[st.session_state.user_id]["login_time"] = datetime.utcnow()
    
    

# ------------------------------------------------------------------
# 10. Функция очистки истёкших корзин
# ------------------------------------------------------------------
def cleanup_expired_carts():
    current_time = datetime.utcnow()
    for uid, data in ss.users.items():
        if current_time - data["login_time"] > timedelta(hours=0, minutes=CLEANUP_TIME):
            # Восстановление запасов
            for pid, qty in data["cart"].items():
                ss.stock[pid] = ss.stock.get(pid, 0) + qty
                data["cart"][pid] = 0  # Очистка корзины
            # Обновление времени входа
            data["login_time"] = current_time  # Обновляем время, чтобы не очищать снова

def cleanup_payed_cart(user_id):
    current_time = datetime.utcnow()
    for uid, data in ss.users.items():
        if str(uid) == str(user_id):    
        #if current_time - data["login_time"] > timedelta(hours=0, minutes=CLEANUP_TIME):
            # Восстановление запасов
            for pid, qty in data["cart"].items():
                #ss.stock[pid] = ss.stock.get(pid, 0) + qty
                data["cart"][pid] = 0  # Очистка корзины
            # Обновление времени входа
            data["login_time"] = current_time  # Обновляем время, чтобы не очищать снова


# Вызов функции очистки при запуске приложения
cleanup_expired_carts()


with tab_hello:
    #status_code = st.query_params.get("o_st", "")
    order_id = st.query_params.get("o_id", "")

    if order_id == "":
        st.title("Добро пожаловать")
        st.write("Если вы ранее не начинали покупок , просто перейдите на вкладку '🛍 Товары' и начните!!!")
        st.write(" ")
        st.write("Если вы обновили страницу и хотите продолжить покупки с существующей корзиной , вам поможет раздел 'Продолжить покупки'.")
        
        st.subheader("Продолжить покупки")
        #with st.expander("Продолжить покупки"):
            #st.markdown("Введите существующий id, если вы уже начали заполнять корзину ранее")
        new_u_id = st.text_input("Введите существующий id, если вы уже начали заполнять корзину ранее")
        msg = " "
        if new_u_id == "":
            pass
        elif new_u_id not in ss.users:
            msg = "Корзина с таким id не найдена"
            #new_u_id = u_id
        else:
            msg = "Корзина найдена"
            st.session_state.user_id = new_u_id
            # user_id = st.session_state.user_id
        st.write(msg)

        st.warning(f'Будьте внимательны : Неоплаченные необновляемые корзины очищаются после {CLEANUP_TIME} минут бездействия')
    else: 
        if st.session_state.no_more_cart_cleaning == False:
            cleanup_payed_cart(st.session_state.user_id)
            st.session_state.no_more_cart_cleaning = True
        st.success(f"Заказ {order_id} оплачен")


# ------------------------------------------------------------------
# 11. Вкладка «Товары»
# ------------------------------------------------------------------
with tab_products:
    st.title("🛍 Товары")
    st.write(f"Ваш ID: **{st.session_state.user_id}**")
    # Фильтры
    selected_category = st.selectbox("Категория", categories, index=0, label_visibility="visible")
    selected_country = st.selectbox("Страна производства", countries, index=0, label_visibility="visible")
    selected_brand = st.selectbox("Бренд", brands, index=0, label_visibility="visible")
    
    # Фильтрация
    display_products = products
    if selected_category != "Все":
        display_products = [p for p in display_products if p["category"] == selected_category]
    if selected_country != "Все":
        display_products = [p for p in display_products if p["country"] == selected_country]
    if selected_brand != "Все":
        display_products = [p for p in display_products if p["brand"] == selected_brand]
    
    if not display_products:
        st.info("По выбранным фильтрам товаров нет.")
    else:
        cols = st.columns(2)
        for i, p in enumerate(display_products):
            col = cols[i % 2]
            with col:
                im_name = f"{str(p['id'])[1:]}_0"
                im_p = f"i/{im_name}.txt"

                if Path(im_p).exists():
                    im_bytes = l_1(im_name, f"{im_name}.txt")
                    st.image(im_bytes, 
                            use_container_width=True #width=50
                            )
                else:
                    st.image(generate_image(p["color"]), use_container_width=True)
                
                # # Описание товара
                # with st.expander("ℹ Описание"):
                #     #st.write(p["desc"])
                #     st.write(f"🧪 Состав: {p['composition']}")
                #     st.write(f"🌍 Страна: {p['country']}")
                #     st.write(f"🏷 Бренд: {p['brand']}")
                
                # st.write(f"**{p['name']}**")
                # Цена
                # Первая цифра ID определяет валюту
                # currency_type = get_currency_type(str(p["id"]))
                # if currency_type == 1:
                #     currency_display = "💲 "
                # elif currency_type == 2:
                #     currency_display = "❤️ "
                # elif currency_type == 3:
                #     currency_display = "💧 "
                # else:
                #     currency_display = ""
                # st.write(f"{currency_display}{p['price']}")
                # currency_type = get_currency_type(str(p["id"]))
                # if currency_type == 1:
                    # p["price"] — словарь {USD:…, RUB:…}
                mul = convert_currency2(p["price"]["MUL"], p["price"]["MUL_cur"], st.session_state.preferred_cur[0:3]) #p["price"]["MUL"]
                #mul_cur = p["price"]["MUL_cur"] # of seller
                mul_cur = st.session_state.preferred_cur[0:3]
                nik = p["price"]["NSN"]
                bon = p["price"]["BON"]
                nik_cur = "NSN"
                bon_cur = "BON"
                if p["sale_coef"]["MUL"] != 1:
                    mul_sale = f'**{round(p["sale_coef"]["MUL"] * mul, 2)}**'
                    mul = f"~{mul}~ "
                else:
                    mul_sale = ""

                if p["sale_coef"]["NSN"] != 1:
                    nik_sale = f'**{math.ceil(p["sale_coef"]["NSN"] * nik)}**'
                    nik = f"~{nik}~ "
                else:
                    nik_sale = ""

                if p["sale_coef"]["BON"] != 1:
                    bon_sale = f'**{math.ceil(p["sale_coef"]["BON"] * bon)}**'
                    bon = f"~{bon}~ "
                else:
                    bon_sale = ""
                        
                st.badge(f"🏷️ {mul} {mul_sale} **{mul_cur}** / {nik} {nik_sale} **{nik_cur}**  /  {bon} {bon_sale} **{bon_cur}** ",
                         color="violet"#"primary"
                         )
                st.write(f"**{p['name']}**")

                # Описание товара
                with st.expander("ℹ &nbsp; Характеристики товара"):
                    #st.write(p["desc"])
                    st.write(f"🧪 Состав: {p['composition']}")
                    st.write(f"🌍 Страна: {p['country']}")
                    st.write(f"🏷 Бренд: {p['brand']}")
                
                
                # Кнопки «подробнее»
                def make_dialog(prod):
                    #@st.dialog(f"Подробнее о {prod['name']}")
                    @st.dialog(f"\n{prod['name']}")
                    def _dialog():
                        #st.title(f"\n{prod['name']}")
                        small_imgs = []
                        big_imgs = []

                        im_name = f"{str(prod['id'])[1:]}" 

                        if Path(f"i/{im_name}_0.txt").exists():
                            for i in range(10):
                                im_name_1 = f"{str(prod['id'])[1:]}_{i}"
                                im_p = f"i/{im_name_1}.txt"

                                if Path(im_p).exists():
                                    im_bytes = l_1(im_name_1, f"{im_name_1}.txt")
                                    im = Image.open(io.BytesIO(im_bytes))
                                    big_imgs.append(im)

                                    small_im = im.resize((150, 150))
                                    small_imgs.append(small_im)

                        else:
                            im = generate_image(prod["color"], size=300)
                            big_imgs.append(im)
                            small_imgs.append(im.resize((150, 150)))


                        # im_1 = generate_image([128,255,128], size=5)
                        # im_2 = generate_image([128,128,128], size=5)
                        # small_imgs = [im_1, im_2]
                        # im_1_big = generate_image([128,255,128])
                        # im_2_big = generate_image([128,128,128])
                        # big_imgs = [im_1_big, im_2_big]
                        sel_index = image_select("", small_imgs, 
                                               use_container_width=False,
                                               return_value="index")
                        
                        #st.write(sel_img)
                        #st.write(sel_index)
                        st.image(big_imgs[sel_index], 
                                 #width=300
                                 )
                        #st.image(generate_image(prod["color"], size=300), width=300)
                        st.write(prod["desc"])
                        st.write(f"🧪 **Состав:** {prod['composition']}")
                        st.write(f"🌍 **Страна:** {prod['country']}")
                        st.write(f"🏷 **Бренд:** {prod['brand']}")
                        
                        mul = convert_currency2(p["price"]["MUL"], p["price"]["MUL_cur"], st.session_state.preferred_cur[0:3]) #p["price"]["MUL"]
                        #mul_cur = p["price"]["MUL_cur"] # of seller
                        mul_cur = st.session_state.preferred_cur[0:3]
                        nik = p["price"]["NSN"]
                        bon = p["price"]["BON"]
                        nik_cur = "NSN"
                        bon_cur = "BON"
                        if p["sale_coef"]["MUL"] != 1:
                            mul_sale = f'**{round(p["sale_coef"]["MUL"] * mul, 2)}**'
                            mul = f"~{mul}~ "
                        else:
                            mul_sale = ""

                        if p["sale_coef"]["NSN"] != 1:
                            nik_sale = f'**{math.ceil(p["sale_coef"]["NSN"] * nik)}**'
                            nik = f"~{nik}~ "
                        else:
                            nik_sale = ""

                        if p["sale_coef"]["BON"] != 1:
                            bon_sale = f'**{math.ceil(p["sale_coef"]["BON"] * bon)}**'
                            bon = f"~{bon}~ "
                        else:
                            bon_sale = ""

                        # st.write(f"🏷️ {mul} {mul_cur} / {nik} {nik_cur} / {bon} {bon_cur}")
                        #st.badge(f"🏷️ {mul}{mul_sale} {mul_cur} / {nik}{nik_sale} {nik_cur} / {bon}{bon_sale} {bon_cur}")
                        st.badge(f"🏷️ {mul} {mul_sale} **{mul_cur}** / {nik} {nik_sale} **{nik_cur}**  /  {bon} {bon_sale} **{bon_cur}** ",
                         color="violet"#"primary"
                         )
                        # elif ctype == 2:
                        #     st.write(f"❤️ **Цена:** {prod['price']} шт.")
                        # else:
                        #     st.write(f"💧 **Цена:** {prod['price']} л.")
                    return _dialog
                
                if st.button("Подробнее", key=f"details_{p['id']}", 
                             width="stretch"):
                    make_dialog(p)()
                
                # Кнопки «Купить»
                if p["category"] == "Книги":
                    # Бумажная версия
                    key_paper = f"{p['id']}_paper"
                    avail_paper = ss.stock.get(key_paper, 0)
                    btn_text_paper = "Купить бумажную" if avail_paper > 0 else "Нет в наличии"
                    btn_disabled_paper = avail_paper <= 0 and avail_paper != 0.5
                    st.button(
                        btn_text_paper,
                        key=f"buy_{key_paper}",
                        disabled=btn_disabled_paper,
                        on_click=buy_callback,
                        args=(str(p["id"]), "paper"),
                        type="primary", 
                        width="stretch"
                    )
                    
                    # Электронная версия
                    key_e = f"{p['id']}_e"
                    avail_e = ss.stock.get(key_e, 0)
                    btn_text_e = "Купить электронную" if avail_e > 0 else "Нет в наличии"
                    btn_disabled_e = avail_e <= 0 and avail_e != 0.5
                    st.button(
                        btn_text_e,
                        key=f"buy_{key_e}",
                        disabled=btn_disabled_e,
                        on_click=buy_callback,
                        args=(str(p["id"]), "e"),
                        type="primary", 
                        width="stretch"
                    )

                elif p["category"] == "Аудиокниги":
                    # версия a
                    key_opta = f"{p['id']}_opta"
                    avail_opta = ss.stock.get(key_opta, 0)
                    btn_text_opta = "Купить версию БЕЗ рекламы" if avail_opta > 0 else "БЕЗ рекламы разобрали"
                    btn_disabled_opta = avail_opta <= 0 and avail_opta != 0.5
                    st.button(
                        btn_text_opta,
                        key=f"buy_{key_opta}",
                        disabled=btn_disabled_opta,
                        on_click=buy_callback,
                        args=(str(p["id"]), "opta"),
                        type="primary", 
                        width="stretch"
                    )
                    
                    # версия b
                    key_optb = f"{p['id']}_optb"
                    avail_optb = ss.stock.get(key_optb, 0)
                    btn_text_optb = "Купить версию С рекламой" if avail_optb > 0 else "С рекламой разобрали"
                    btn_disabled_optb = avail_optb <= 0 and avail_optb != 0.5
                    st.button(
                        btn_text_optb,
                        key=f"buy_{key_optb}",
                        disabled=btn_disabled_optb,
                        on_click=buy_callback,
                        args=(str(p["id"]), "optb"),
                        type="primary", 
                        width="stretch"
                    )

                else:
                    key = str(p["id"])
                    avail = ss.stock.get(key, 0)
                    btn_text = "Купить" if avail > 0 else "Нет в наличии"
                    btn_disabled = avail <= 0 and avail != 0.5
                    st.button(
                        btn_text,
                        key=f"buy_{key}",
                        disabled=btn_disabled,
                        on_click=buy_callback,
                        args=(key, None),
                        type="primary", 
                        width="stretch"
                    )
                st.write("")
                st.write("")
                st.write("")

# ------------------------------------------------------------------
# 12. Вкладка «Корзина»
# ------------------------------------------------------------------
with tab_cart:
    st.title("🛒 Корзина")
    if dev_mode == 1:
       st.write(ss.users)
       st.write(ss.stock)
    #cart_usd, cart_hearts, cart_water = split_cart_by_currency()
    user_cart = ss.users[st.session_state.user_id]["cart"]
    
    total_items = sum(user_cart.values()) 
    if total_items == 0:
        st.info("Ваша корзина пока пустая.")
        st.stop()
    
    
    # Отображение корзины по частям
    def display_cart_part(cart, cur, conditions, extra_sale_coef):
        if not cart:
            return None, 0
        st.subheader(f"Выбранные товары")
        st.markdown("---")

        # st.write(extra_sale_coef)
        total_part = 0
        for pid, qty in cart.items():
            if qty == 0:
                continue
            # находим продукт
            if "_paper" in pid or "_e" in pid:
                base, vtype = pid.split("_")
                prod = next(p for p in products if str(p["id"])==base)
                name = f"{prod['name']} ({'бумажная' if vtype=='paper' else 'электронная'})"
                brand = prod['brand']
            elif "_opta" in pid or "_optb" in pid:
                base, vtype = pid.split("_")
                prod = next(p for p in products if str(p["id"])==base)
                name = f"{prod['name']} ({'без рекламы' if vtype=='opta' else 'с рекламой'})"
                brand = prod['brand']
            else:
                base = pid
                prod = next(p for p in products if str(p["id"])==pid)
                name = prod["name"]
                brand = prod['brand']

            #Если промокод
            if conditions:
                counter = 0
                fulfilled = 0
                if 'brand' in conditions:
                    counter += 1
                    if conditions['brand'] == brand:
                        fulfilled += 1
                    # else:
                    #     fulfilled += 0
                if 'seller_id' in conditions:
                    counter += 1
                    if str(conditions['seller_id']) == str(pid)[1:3]:
                        fulfilled += 1
                if 'excluded_items' in conditions:
                    counter += 1
                    if int(base) not in conditions['excluded_items']:
                        fulfilled += 1
                if 'included_items' in conditions:
                    counter += 1
                    if int(base) in conditions['included_items']:
                        fulfilled += 1
                if 'expiration_day' in conditions:
                    counter += 1
                    cur_time = datetime.utcnow() + timedelta(hours=st.secrets['hours'])
                    cur_day = cur_time.date()
                    last_day = datetime.strptime(conditions['expiration_day'], "%Y-%m-%d").date()
                    if cur_day <= last_day:
                        fulfilled += 1               

                if counter == fulfilled:
                    st.success("Промокод применён к данному товару")
                    extra_sale_for_item = extra_sale_coef
                else:
                    st.warning(f"Промокод не действует на данный товар. Выполнено {fulfilled}/{counter} условий промокода")
                    extra_sale_for_item = {'MUL': 1, 'NSN': 1, 'BON': 1}
            else:
                # Не введён промокод
                extra_sale_for_item = {'MUL': 1, 'NSN': 1, 'BON': 1}
            #st.write(extra_sale_for_item)

            #ctype = get_currency_type(prod["id"])
            #if ctype == 1:
            if cur != "NSN" and cur != "BON":
                #unit_price = prod["price"]["MUL"]
                unit_price = convert_currency2(extra_sale_for_item["MUL"] * prod["sale_coef"]["MUL"] * prod["price"]["MUL"], 
                                               prod["price"]["MUL_cur"], 
                                               cur)
                sym = cur
            else:
                #unit_price = math.ceil(extra_sale_for_item[cur] * prod["sale_coef"][cur] * prod["price"][cur])
                unit_price = extra_sale_for_item[cur] * prod["sale_coef"][cur] * prod["price"][cur]
                sym = cur

            unit_price = round(unit_price, 2)
            # elif ctype == 2:
            #     unit_price = prod["price"]
            #     sym = "❤️"
            # else:
            #     unit_price = prod["price"]
            #     sym = "💧"

            line_total = unit_price * qty
            total_part += line_total

            # col_name, col_minus, col_qty, col_plus = st.columns([3,0.7,0.6,0.7])
            # with col_name:
            st.write(f"{name} — {unit_price} {sym}")

            with st.container(horizontal=True, 
                              vertical_alignment="bottom", 
                              #border=True,
                              horizontal_alignment="left",
                              width=500):
            # with col_minus:
                def dec(pid_inner=pid):
                    if ss.users[st.session_state.user_id]["cart"][pid_inner] > 0:
                        ss.users[st.session_state.user_id]["cart"][pid_inner] -= 1
                        ss.stock[pid_inner] = ss.stock.get(pid_inner,0) + 1
                        ss.users[st.session_state.user_id]["login_time"] = datetime.utcnow()
                        #st.experimental_rerun()
                st.button("➖", key=f"dec_{pid}", on_click=dec, width=50)
            # with col_qty:
                st.text_input("", value=str(ss.users[st.session_state.user_id]["cart"][pid]),
                            key=f"qty_{pid}", disabled=True, label_visibility="collapsed",
                            width=50)
            # with col_plus:
                if not pid.startswith("ticket_"):
                    base, vtype = pid.split("_")
                    def inc(pid_inner=base):
                        prod = next(p for p in products if str(p["id"])==pid_inner)
                        max_items_per_one_order = prod['max_items']

                        if ss.stock.get(pid_inner,0) <= 0:
                            st.toast("Больше добавить не получится, нет столько товаров")
                            return
                        elif ss.users[st.session_state.user_id]["cart"][pid_inner] + 1 > max_items_per_one_order:
                            st.toast(f"🤫 *в одном заказе может быть не более {max_items_per_one_order} таких товаров*")
                            return
                        
                        ss.stock[pid_inner] -= 1
                        ss.users[st.session_state.user_id]["cart"][pid_inner] += 1
                        ss.users[st.session_state.user_id]["login_time"] = datetime.utcnow()
                        #st.experimental_rerun()
                    st.button("➕", key=f"inc_{pid}", on_click=inc, width=50)

            if qty > 0:
                st.write(f"**{qty}** × {unit_price} {sym} = **{line_total} {sym}**")
                st.markdown("---")

        if cur != "NSN" and cur != "BON":
            total_part = round(total_part, 2)
        else: 
            total_part = math.ceil(total_part)

        return total_part

    # --- вызовы ---
    cur_ = st.radio(
                "Выберите валюту оплаты* :",
                [
                 st.session_state.preferred_cur,
                 #f'{st.session_state.preferred_cur}, {st.secrets.cur[st.session_state.preferred_cur]["forms"][4]}',
                 f'NSN, {st.secrets.cur["NSN"]["forms"][4]}', 
                 f'BON, {st.secrets.cur["BON"]["forms"][4]}'
                 ],
                key="currency_choice"
            )
    cur = cur_[0:3]
    st.caption("\*Если вы имеете мультивалютную карту и хотите оплатить в другой валюте , то выберите нужную валюту в меню 'Показывать международные цены в валюте :', после этого валюта появится в списке.")
    
     #Промокод:
    st.session_state.word = st.text_input("Есть промокод? Введите", value="", 
                        placeholder="ПРОМОКОД",
                        #label_visibility="hidden"
                        )
    st.caption("Обратите внимание, что цены в NSN и BON после применения промокода округляются до целого числа вверх")
    
    conditions = None
    extra_sale_coef = {'MUL': 1, 'NSN': 1, 'BON': 1}
    if st.session_state.word != "":
        for promo in promos:
            if st.session_state.word == promo["word"]:
                st.success("Промокод существует")
                st.info(f"Условия акции : {promo['desc']}")
                #for k, v in promo["conditions"].items():
                    # st.write(f"{k} === {v}")
                conditions = promo["conditions"]
                extra_sale_coef = promo["extra_sale_coef"]
    else:
        pass
        #extra_sale_coef = {'MUL': 1, 'NSN': 1, 'BON': 1}


    sum_total = display_cart_part(user_cart, cur, conditions, extra_sale_coef)

    if sum_total:
        st.write(f"**ИТОГО К ОПЛАТЕ: {sum_total} {cur}**")
        
    
    # ---------------------- Оформление ----------------------
    if st.button("Перейти к оформлению"):
        st.session_state.show_address = True


    if not st.session_state.show_address:
            # Обновление времени входа (для предотвращения повторной очистки)
            #ss.users[st.session_state.user_id]["login_time"] = datetime.utcnow()
            pass
    else:
        st.title("📦 Доставка")

        st.session_state.name = st.text_input("Как вас зовут?", value="", 
                        placeholder=st.secrets["placeholder_name"],
                        #label_visibility="hidden"
                        )
        st.write("Вы можете выбрать адрес , **нажав точку на карте** (карту можно листать влево-вправо). Также вы можете заполнить адрес вручную , если вашего адреса нет на картах или вы хотите добавить деталей.")

        # Выбор адреса
        addr()

        if st.session_state["street"] in st_dict.keys():
            st.session_state["ind"] = st_dict[st.session_state["street"]]
            #st.write(ind)
        else:
            st.session_state["ind"] = None

        address_country = st.text_area("Введите страну доставки", key="country_input",
                                    height=68, 
                                    value=st.session_state["country"])
        # address_country = st.selectbox("Выберите страну доставки из списка или введите другую", key="country_input", 
        #                                 #index=st.session_state["ind"],#ind,
        #                                 help="",
        #                                 options=COUNTRIES,
        #                                 accept_new_options=True
        #                                 )  
        #if st.session_state["country"] in [COUNTRIES[1], ""]:
        if address_country not in [COUNTRIES[0], COUNTRIES[2]]:
            address_city = st.text_area("Введите город доставки", key="city_input", 
                                        height=68,
                                    value=st.session_state["city"])
        # @st.fragment()    
        # def fr():

        col1, col2, col3 = st.columns([0.35,0.55,0.2], vertical_alignment='center')

        with col3:
            if "потолкоскрёб" in st.session_state["extra"]:
                st.session_state["floor"] = st.selectbox("Выберите этаж", 
                                                        options=["1","2","3","4","5","6","крыша"], 
                                                        #on_change=exception_street_callback()
                                                        )
                if st.session_state["floor"]=="5" and PLACES["pts_36"] in st.session_state["extra"]:
                    #st.write(123)
                    st.session_state["street"] = STREETS[7]
                    st.session_state["ind"] = 7
                elif st.session_state["floor"]!="5" and PLACES["pts_36"] in st.session_state["extra"]:
                    st.session_state["street"] = STREETS[0]
                    st.session_state["ind"] = 1

        with col1:
            if st.session_state["country"] not in [COUNTRIES[2]]: # and (PLACES["pts_36"] not in st.session_state["extra"]):    
                # address_street = st.text_area("Введите улицу доставки1", key="street_input1", 
                #                         value=st.session_state["street"],
                #                         height=68,
                #                         #on_change=exception_street_callback(),
                #                         #options=[STREETS[7], STREETS[0]]
                #               ) 
                if st.session_state["country"] in [COUNTRIES[0]]:
                    address_street = st.selectbox("Введите улицу доставки", key="street_input1", 
                                        index=st.session_state["ind"],#ind,
                                        help="",
                                        #height=68,
                                        #on_change=exception_street_callback(),
                                        options=st_l,
                                        accept_new_options=True
                                        )  
                else:
                    address_street = st.text_area("Введите улицу доставки", key="street_input2",
                                    height=68, 
                                    value=st.session_state["street"])
                #st.selectbox() 
        # if st.session_state["country"] not in [COUNTRIES[2]] and (PLACES["pts_36"] in st.session_state["extra"]) and st.session_state["floor"]=="5":   
        #     st.session_state["street"] = STREETS[7]
        #     address_street = st.text_input("Введите улицу доставки2", key="street_input2", 
        #                                 value=st.session_state["street"],
        #                                 #on_change=exception_street_callback()
        #                                 )  
        # if st.session_state["country"] not in [COUNTRIES[2]] and (PLACES["pts_36"] in st.session_state["extra"]) and st.session_state["floor"]!="5":   
        #     st.session_state["street"] = STREETS[0]
        #     address_street = st.text_input("Введите улицу доставки3", key="street_input3", 
        #                                 value=st.session_state["street"],
        #                                 #on_change=exception_street_callback()
        #                                 )  
        with col2:
            address_extra = st.text_area("Введите дополнительную информацию при наличии", key="extra_input", 
                                        value=st.session_state["extra"],
                                        height=68,
                                        )
            
        address_floor = st.session_state["floor"]

        full_addr2 = ""

        fields = []
        country_id = ""
        city_id = ""
        street_id =""
        extra_id = ""
        #floor_id = ""

        if 'address_country' in locals():
            fields.append(address_country)
            if address_country in COUNTRIES:
                country_id = str(COUNTRIES.index(address_country))
            else: 
                country_id = enc(address_country)

        if 'address_city' in locals():
            fields.append(address_city)
            if address_city in CITIES:
                city_id = str(CITIES.index(address_city))
            elif "г." + address_city in CITIES:
                city_id = str(CITIES.index("г." + address_city))
            else: 
                city_id = enc(address_city)

        if 'address_street' in locals():
            fields.append(address_street)
            if address_street in STREETS:
                street_id = str(STREETS.index(address_street))
            elif "ул." + address_street in STREETS:
                street_id = str(STREETS.index("ул." + address_street))
            else: 
                street_id = enc(address_street)

        if 'address_extra' in locals():
            fields.append(address_extra)
            for k,v  in PLACES.items():
                if v == address_extra:
                    extra_id = k
                else: 
                    extra_id = enc(address_extra)
            if 'address_floor' in locals():
                if address_floor.isdigit(): # != "" and address_extra != "":
                    fields.append(address_floor + " этаж")
                else: 
                    fields.append(address_floor)


        for i in fields:
            if i != "":
                full_addr2 += i + ', '

        full_addr2 = full_addr2[0: -2]  
        st.write(full_addr2)
        
        posts = []
        bios = []
        regions = []
        for i in POST_SERVICES:
            posts.append(i["name"])
            #bios.append(str(i["regions"]))
            bios.append(i["desc"])
            #regions.append(i["regions"])

        selected_post = st.radio("Выберите службу доставки", 
                                posts, 
                                horizontal=False, 
                                captions=bios,
                                #index=st.session_state["card_index"],
                                #key="card_type_radio",
                                #on_change=on_change()
                                )
        #st.write(selected_post)

        post_serv = next(ps for ps in POST_SERVICES if str(ps["name"])==selected_post)

        if post_serv['regions'][0] != "all":
            if any(reg.lower() in full_addr2.lower() for reg in post_serv['regions']):
                delivery = True
            else:
                delivery = False
                st.warning("Нет доставки на выбранный адрес. Выберите другую службу доставки")
        else:
           delivery = True
        
        if st.button("Перейти к оплате"):
            # Обновление времени входа (для предотвращения повторной очистки)
            ss.users[st.session_state.user_id]["login_time"] = datetime.utcnow()
            

            endpoint = st.secrets["endpoint"]

            if len(st.session_state.name) > 1:
                if address_country != "":
                    if delivery:
                        def cart_link(cart_part, selected_cur):
                            cart_str = ";".join(
                                f"{pid},{qty}" for pid, qty in cart_part.items() if qty > 0
                            )
                            link = f"{endpoint}?cart={urllib.parse.quote(cart_str)}&cur={selected_cur}&time={ss.users[st.session_state.user_id]['login_time']}&post={post_serv['id']}&addr_1={urllib.parse.quote(country_id)}&addr_2={urllib.parse.quote(city_id)}&addr_3={urllib.parse.quote(street_id)}&addr_4={urllib.parse.quote(extra_id)}&addr_5={urllib.parse.quote(address_floor)}&name={enc(st.session_state.name)}&word={st.session_state.word}&user_id={st.session_state.user_id}"
                            return link
                
                        # ---------------------- Оплата ----------------------
                        st.markdown("### Оплата корзины")
                        
                        accepted_methods_im_name = "1"

                        im_bytes_accepted = l_1(accepted_methods_im_name, f"{accepted_methods_im_name}.txt")

                        st.image(im_bytes_accepted,  
                                    caption="Принимаемые способы оплаты",
                                    width=200)
                        
                        if user_cart:
                            link = cart_link(user_cart, cur)
                            st.link_button("💳 Оплатить", link)
                    else: 
                        st.error("Нет доставки на выбранный адрес. Выберите другую службу доставки")
                else: 
                    st.error("Заполните адрес")
            else: 
                st.error("Заполните поле имени")
            
