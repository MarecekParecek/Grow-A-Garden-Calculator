import customtkinter as ctk
from PIL import Image
import os

PRIMARY_COLOR = "#3a6a3a"
ACCENT_COLOR = "#e4fa55"
TEXT_COLOR = "#000000"
SIGNATURE_COLOR = "#ffffff"
TITLE_COLOR = "#ffffff"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

fruits_by_rarity = {
    "Common": {"Carrot": 18, "Strawberry": 14},
    "Uncommon": {"Blueberry": 18, "Orange Tulip": 767},
    "Rare": {"Tomato": 27, "Corn": 36, "Daffodil": 903},
    "Legendary": {"Watermelon": 2708, "Pumpkin": 3700, "Apple": 248, "Bamboo": 3610},
    "Mythical": {"Coconut": 361, "Cactus": 3068, "Dragon fruit": 4287, "Mango": 5866, "Peach": 271, "Pineapple": 1805},
    "Divine": {"Grape": 7085, "Mushroom": 136278, "Pepper": 7220, "Cacao": 9928},
    "Prismatic": {"Beanstalk": 18050},
    "Limited": {
        "Cranberry": 1805, "Durian": 4513, "EasterEgg": 4513, "Moonflower": 8500, "Starfruit": 15538,
        "Papaya": 1000, "Eggplant": 6769, "Moonglow": 18000, "Passionfruit": 3204, "Lemon": 500,
        "Banana": 1579, "BloodBanana": 5415, "MoonMelon": 16245, "MoonBlossom": 45125,
        "CherryBlossom": 550, "CandyBlossom": 93567, "Lotus": 20000, "VenusFlyTrap": 17000,
        "CursedFruit": 15000, "SoulFruit": 3000
    }
}

growth_mutations = {
    "None": 1,
    "Golden": 25,
    "Rainbow": 50
}

env_stack_values = {
    "Wet": 1, "Chilled": 1, "Chocolate": 1, "Moonlit": 1,
    "Bloodlit": 3, "Plasma": 4, "Frozen": 9, "Zombified": 24,
    "Shocked": 99, "Celestial": 119, "Disco": 124
}

BUTTON_WIDTH = int(180 * 1.25)

class GrowAGardenApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Grow a Garden Calculator")
        self.geometry("700x700")
        self.minsize(700, 700)
        self.configure(fg_color=PRIMARY_COLOR)

        self.selected_rarity = None
        self.selected_fruit = None
        self.base_value = 0
        self.growth_mult = 1
        self.selected_env = []

        self.frames = {}
        for F in (StartPage, FruitPage, GrowthMutationPage, EnvironmentalMutationPage, ResultPage):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class BasePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=PRIMARY_COLOR)
        self.signature = ctk.CTkLabel(self, text="by Faru",
                                      font=ctk.CTkFont(size=40, weight="bold"),
                                      text_color=SIGNATURE_COLOR)
        self.signature.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

class StartPage(BasePage):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        center_frame = ctk.CTkFrame(self, fg_color=PRIMARY_COLOR)
        center_frame.grid(row=0, column=0)
        center_frame.grid_rowconfigure(0, weight=1)
        center_frame.grid_columnconfigure(0, weight=1)

        inner_frame = ctk.CTkFrame(center_frame, fg_color=PRIMARY_COLOR)
        inner_frame.grid(row=0, column=0, padx=40, pady=40)

        logo_path = os.path.join(os.path.dirname(__file__), "Site-community-image.png")
        if os.path.exists(logo_path):
            image = ctk.CTkImage(Image.open(logo_path), size=(625 * 1.25, 250 * 1.25))
            self.logo_label = ctk.CTkLabel(inner_frame, image=image, text="", fg_color=PRIMARY_COLOR)
            self.logo_label.image = image
            self.logo_label.pack(pady=(5, 5))

        title = ctk.CTkLabel(inner_frame, text="Select Rarity", font=ctk.CTkFont(size=28, weight="bold"), text_color=TITLE_COLOR)
        title.pack(pady=15)

        btn_frame = ctk.CTkFrame(inner_frame, fg_color=PRIMARY_COLOR)
        btn_frame.pack()

        for rarity in fruits_by_rarity:
            btn = ctk.CTkButton(btn_frame, text=rarity,
                                fg_color="white", text_color=TEXT_COLOR,
                                hover_color=ACCENT_COLOR,
                                corner_radius=15,
                                command=lambda r=rarity: self.select_rarity(r),
                                width=BUTTON_WIDTH)
            btn.pack(pady=5)

    def select_rarity(self, rarity):
        self.master.selected_rarity = rarity
        self.master.show_frame(FruitPage)

class FruitPage(BasePage):
    def __init__(self, master):
        super().__init__(master)
        self.inner_frame = ctk.CTkFrame(self, fg_color=PRIMARY_COLOR)
        self.inner_frame.pack(expand=True)

        self.label = ctk.CTkLabel(self.inner_frame, text="", font=ctk.CTkFont(size=22, weight="bold"), text_color=TITLE_COLOR)
        self.label.pack(pady=10)

        self.back_button = ctk.CTkButton(self.inner_frame, text="← Back", fg_color="white", text_color=TEXT_COLOR,
                                         hover_color=ACCENT_COLOR, corner_radius=15,
                                         command=lambda: master.show_frame(StartPage))
        self.back_button.pack(pady=5)

        self.fruit_buttons = []

    def update_buttons(self):
        for btn in self.fruit_buttons:
            btn.destroy()
        self.fruit_buttons.clear()

        rarity = self.master.selected_rarity
        self.label.configure(text=f"Select Fruit from {rarity}")
        for fruit, value in fruits_by_rarity[rarity].items():
            btn = ctk.CTkButton(self.inner_frame, text=f"{fruit} ({value})",
                                fg_color="white", text_color=TEXT_COLOR,
                                hover_color=ACCENT_COLOR, corner_radius=15,
                                command=lambda f=fruit, v=value: self.select_fruit(f, v),
                                width=BUTTON_WIDTH)
            btn.pack(pady=3)
            self.fruit_buttons.append(btn)

    def tkraise(self, *args, **kwargs):
        self.update_buttons()
        super().tkraise(*args, **kwargs)

    def select_fruit(self, fruit, value):
        self.master.selected_fruit = fruit
        self.master.base_value = value
        self.master.show_frame(GrowthMutationPage)

class GrowthMutationPage(BasePage):
    def __init__(self, master):
        super().__init__(master)
        self.inner_frame = ctk.CTkFrame(self, fg_color=PRIMARY_COLOR)
        self.inner_frame.pack(expand=True)

        title = ctk.CTkLabel(self.inner_frame, text="Select Growth Mutation", font=ctk.CTkFont(size=22, weight="bold"), text_color=TITLE_COLOR)
        title.pack(pady=15)

        back_btn = ctk.CTkButton(self.inner_frame, text="← Back", fg_color="white", text_color=TEXT_COLOR,
                                 hover_color=ACCENT_COLOR, corner_radius=15,
                                 command=lambda: master.show_frame(FruitPage))
        back_btn.pack(pady=5)

        for mut, mult in growth_mutations.items():
            btn = ctk.CTkButton(self.inner_frame, text=f"{mut} ×{mult}",
                                fg_color="white", text_color=TEXT_COLOR,
                                hover_color=ACCENT_COLOR, corner_radius=15,
                                command=lambda m=mult: self.select_mutation(m),
                                width=BUTTON_WIDTH)
            btn.pack(pady=4)

    def select_mutation(self, mult):
        self.master.growth_mult = mult
        self.master.show_frame(EnvironmentalMutationPage)

class EnvironmentalMutationPage(BasePage):
    def __init__(self, master):
        super().__init__(master)
        self.inner_frame = ctk.CTkFrame(self, fg_color=PRIMARY_COLOR)
        self.inner_frame.pack(expand=True)

        title = ctk.CTkLabel(self.inner_frame, text="Select Environmental Mutations", font=ctk.CTkFont(size=22, weight="bold"), text_color=TITLE_COLOR)
        title.pack(pady=10)

        self.vars = {}
        back_btn = ctk.CTkButton(self.inner_frame, text="← Back", fg_color="white", text_color=TEXT_COLOR,
                                 hover_color=ACCENT_COLOR, corner_radius=15,
                                 command=lambda: master.show_frame(GrowthMutationPage))
        back_btn.pack(pady=5)

        for mut in env_stack_values:
            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(self.inner_frame, text=mut, variable=var, text_color=TEXT_COLOR, fg_color=PRIMARY_COLOR,
                                 hover_color=ACCENT_COLOR)
            cb.pack(anchor="w", padx=10)
            self.vars[mut] = var

        confirm_btn = ctk.CTkButton(self.inner_frame, text="Confirm", fg_color=ACCENT_COLOR, text_color=TEXT_COLOR,
                                    corner_radius=15, command=self.confirm, width=BUTTON_WIDTH)
        confirm_btn.pack(pady=15)

    def confirm(self):
        selected = [mut for mut, var in self.vars.items() if var.get()]
        exclusive = [m for m in selected if m in {"Wet", "Chilled", "Frozen"}]
        if len(exclusive) > 1:
            from tkinter import messagebox
            messagebox.showinfo("Warning", "Only one of Wet/Chilled/Frozen is allowed. Keeping first only.")
            keep = exclusive[0]
            selected = [m for m in selected if m not in {"Wet", "Chilled", "Frozen"}] + [keep]
        self.master.selected_env = selected
        self.master.show_frame(ResultPage)

class ResultPage(BasePage):
    def __init__(self, master):
        super().__init__(master)
        self.inner_frame = ctk.CTkFrame(self, fg_color=PRIMARY_COLOR)
        self.inner_frame.pack(expand=True)

        self.label = ctk.CTkLabel(self.inner_frame, text="", font=ctk.CTkFont(size=18, weight="bold"), text_color=TITLE_COLOR, justify="left")
        self.label.pack(pady=20)

        back_btn = ctk.CTkButton(self.inner_frame, text="← Back", fg_color="white", text_color=TEXT_COLOR,
                                 hover_color=ACCENT_COLOR, corner_radius=15,
                                 command=lambda: master.show_frame(EnvironmentalMutationPage))
        back_btn.pack(pady=5)

        restart_btn = ctk.CTkButton(self.inner_frame, text="Restart", fg_color=ACCENT_COLOR, text_color=TEXT_COLOR,
                                    corner_radius=15, command=lambda: master.show_frame(StartPage))
        restart_btn.pack(pady=10)

    def tkraise(self, *args, **kwargs):
        base_value = self.master.base_value
        growth_mult = self.master.growth_mult
        stack_sum = sum(env_stack_values.get(m, 0) for m in self.master.selected_env)
        total = base_value * growth_mult * (stack_sum if stack_sum > 0 else 1)
        total_str = f"{total:,}".replace(",", " ")

        env_text = ", ".join(self.master.selected_env) if self.master.selected_env else "None"

        result_text = (
            f"Fruit: {self.master.selected_fruit}\n"
            f"Base Value: {base_value}\n"
            f"Growth Mutation Multiplier: {growth_mult}\n"
            f"Environmental Mutations: {env_text}\n"
            f"Environmental Multiplier Sum: {stack_sum if stack_sum > 0 else 1}\n"
            f"Total Value: {total_str}"
        )
        self.label.configure(text=result_text)
        super().tkraise(*args, **kwargs)

if __name__ == "__main__":
    app = GrowAGardenApp()
    app.mainloop()
