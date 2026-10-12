from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
import requests
import time

FIREBASE_URL = "https://mi-app-fae76-default-rtdb.firebaseio.com"
ADMIN_PIN = "7788"
OPAY_NUMBER = "9154609119"

def is_online():
    try:
        requests.get("https://google.com", timeout=3)
        return True
    except:
        return False

KV = '''
ScreenManager:
    MainScreen:
    ProfileScreen:
    NotificationScreen:
    AdminScreen:
    SubScreen:

<MainScreen>:
    name: "main"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 0,0,0,1
        MDTopAppBar:
            title: "Mi App - LIVE"
            left_action_items: [["account", lambda x: setattr(app.root, 'current', 'profile')]]
            right_action_items: [["bell", lambda x: setattr(app.root, 'current', 'notifications')], ["shield-crown", lambda x: setattr(app.root, 'current', 'admin')], ["crown", lambda x: setattr(app.root, 'current', 'sub')]]
        MDBoxLayout:
            orientation: "vertical"
            padding: "20dp"
            spacing: "20dp"
            MDLabel:
                text: "Mi App is Live! Firebase: mi-app-fae76"
                halign: "center"
                bold: True
            MDCard:
                size_hint_y: None
                height: "100dp"
                md_bg_color: 0.08,0.08,0.1,1
                radius: [20]
                padding: "15dp"
                MDBoxLayout:
                    MDBoxLayout:
                        orientation: "vertical"
                        MDLabel:
                            id: fol
                            text: "0"
                            halign: "center"
                            bold: True
                        MDLabel:
                            text: "Followers"
                            halign: "center"
                            font_size: "10sp"
                    MDBoxLayout:
                        orientation: "vertical"
                        MDLabel:
                            id: lik
                            text: "0"
                            halign: "center"
                            bold: True
                        MDLabel:
                            text: "Likes"
                            halign: "center"
                            font_size: "10sp"
                    MDBoxLayout:
                        orientation: "vertical"
                        MDLabel:
                            id: sha
                            text: "0"
                            halign: "center"
                            bold: True
                        MDLabel:
                            text: "Shares"
                            halign: "center"
                            font_size: "10sp"
                    MDBoxLayout:
                        orientation: "vertical"
                        MDLabel:
                            id: msg
                            text: "0"
                            halign: "center"
                            bold: True
                        MDLabel:
                            text: "Messages"
                            halign: "center"
                            font_size: "10sp"
            MDLabel:
                id: status_main
                text: "Loading..."
                halign: "center"
            MDRaisedButton:
                text: "Refresh Stats"
                pos_hint: {"center_x":0.5}
                on_release: root.load_stats()

<ProfileScreen>:
    name: "profile"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 0,0,0,1
        MDTopAppBar:
            title: "Profile & Privacy"
            left_action_items: [["arrow-left", lambda x: setattr(app.root, 'current', 'main')]]
        MDBoxLayout:
            orientation: "vertical"
            padding: "20dp"
            spacing: "15dp"
            MDLabel:
                id: p_status
                text: "Status: Loading..."
                halign: "center"
            MDBoxLayout:
                size_hint_y: None
                height: "50dp"
                spacing: "10dp"
                MDRaisedButton:
                    text: "Online"
                    on_release: root.set_privacy("online")
                MDRaisedButton:
                    text: "Offline"
                    on_release: root.set_privacy("offline")
                MDRaisedButton:
                    text: "Private"
                    on_release: root.set_privacy("private")
            MDLabel:
                id: p_fol
                text: "Followers: 0"
                halign: "center"
            MDLabel:
                id: p_lik
                text: "Likes: 0"
                halign: "center"

<NotificationScreen>:
    name: "notifications"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 0,0,0,1
        MDTopAppBar:
            title: "Notifications"
            left_action_items: [["arrow-left", lambda x: setattr(app.root, 'current', 'main')]]
        ScrollView:
            MDList:
                id: notif_list

<AdminScreen>:
    name: "admin"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 0,0,0,1
        MDTopAppBar:
            title: "Admin Dashboard"
            left_action_items: [["arrow-left", lambda x: setattr(app.root, 'current', 'main')]]
        MDBoxLayout:
            orientation: "vertical"
            padding: "20dp"
            spacing: "10dp"
            MDTextField:
                id: pin_input
                hint_text: "Enter PIN 7788"
                password: True
            MDRaisedButton:
                text: "Unlock"
                on_release: root.unlock()
            MDLabel:
                id: admin_info
                text: "Enter PIN"

<SubScreen>:
    name: "sub"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 0,0,0,1
        MDTopAppBar:
            title: "Mi Sub - OPay"
            left_action_items: [["arrow-left", lambda x: setattr(app.root, 'current', 'main')]]
        MDBoxLayout:
            orientation: "vertical"
            padding: "20dp"
            MDLabel:
                id: opay_label
                text: "OPay"
                halign: "center"
            MDTextField:
                id: proof
                hint_text: "Payment proof"
            MDRaisedButton:
                text: "Verify"
                on_release: root.verify_pay()
'''

class MainScreen(Screen):
    def on_enter(self, *args):
        self.load_stats()
    def load_stats(self):
        try:
            user = MDApp.get_running_app().user_name
            fol_data = requests.get(f"{FIREBASE_URL}/mi_followers/{user}.json").json()
            fol = len(fol_data) if fol_data else 0
            lik = requests.get(f"{FIREBASE_URL}/mi_likes_count/{user}.json").json()
            if lik is None:
                lik = 0
            sha = requests.get(f"{FIREBASE_URL}/mi_shares_count/{user}.json").json()
            if sha is None:
                sha = 0
            msg_data = requests.get(f"{FIREBASE_URL}/mi_chats/{user}.json").json()
            msg = len(msg_data) if msg_data else 0
            pres = requests.get(f"{FIREBASE_URL}/mi_presence/{user}.json").json()
            if pres is None:
                pres = {"status": "online"}
            self.ids.fol.text = str(fol)
            self.ids.lik.text = str(lik)
            self.ids.sha.text = str(sha)
            self.ids.msg.text = str(msg)
            self.ids.status_main.text = f"Status: {pres.get('status','online')}"
        except Exception as e:
            print(e)
            self.ids.status_main.text = "Offline - Check Internet"

class ProfileScreen(Screen):
    def on_enter(self, *args):
        self.load_data()
    def load_data(self):
        try:
            user = MDApp.get_running_app().user_name
            fol_data = requests.get(f"{FIREBASE_URL}/mi_followers/{user}.json").json()
            fol = len(fol_data) if fol_data else 0
            lik = requests.get(f"{FIREBASE_URL}/mi_likes_count/{user}.json").json()
            if lik is None:
                lik = 0
            self.ids.p_fol.text = f"Followers: {fol}"
            self.ids.p_lik.text = f"Likes: {lik}"
            self.ids.p_status.text = f"Current User: {user}"
        except:
            pass
    def set_privacy(self, mode):
        user = MDApp.get_running_app().user_name
        try:
            requests.put(f"{FIREBASE_URL}/mi_presence/{user}.json", json={"status": mode, "last_seen": time.time()})
            requests.post(f"{FIREBASE_URL}/mi_notifications.json", json={"title": "Privacy", "message": f"You are now {mode}", "user": user, "time": time.time()})
            self.ids.p_status.text = f"You are now {mode.upper()}"
        except Exception as e:
            print(e)

class NotificationScreen(Screen):
    def on_enter(self, *args):
        self.load_notifs()
    def load_notifs(self):
        self.ids.notif_list.clear_widgets()
        try:
            from kivymd.uix.list import TwoLineListItem
            data = requests.get(f"{FIREBASE_URL}/mi_notifications.json").json()
            if data is None:
                data = {}
            for k, v in list(data.items())[-15:][::-1]:
                self.ids.notif_list.add_widget(TwoLineListItem(text=v.get("title","Mi App"), secondary_text=v.get("message","")))
        except Exception as e:
            print(e)

class AdminScreen(Screen):
    def unlock(self):
        if self.ids.pin_input.text == ADMIN_PIN:
            self.load_admin()
        else:
            self.ids.admin_info.text = "Wrong PIN"
    def load_admin(self):
        try:
            users = requests.get(f"{FIREBASE_URL}/mi_presence.json").json()
            if users is None:
                users = {}
            count = len(users)
            online = 0
            for u in users.values():
                if u.get("status") == "online":
                    online += 1
            txt = f"Total Users: {count}\nOnline: {online}\n\n"
            for name, info in users.items():
                txt += f"{name}: {info.get('status')}\n"
            self.ids.admin_info.text = txt
        except Exception as e:
            self.ids.admin_info.text = f"Error: {e}"

class SubScreen(Screen):
    def on_enter(self, *args):
        self.ids.opay_label.text = f"Pay to OPay: {OPAY_NUMBER}"
    def verify_pay(self):
        proof = self.ids.proof.text
        if proof == "":
            return
        user = MDApp.get_running_app().user_name
        try:
            requests.post(f"{FIREBASE_URL}/mi_subs.json", json={"user": user, "proof": proof, "time": time.time()})
            self.ids.opay_label.text = "Sent! Wait for admin verify"
        except:
            pass

class MiApp(MDApp):
    user_name = "MiUser_PH"
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        return Builder.load_string(KV)

MiApp().run()