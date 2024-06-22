from tkinter import *
from tkinter import messagebox
import mysql.connector


class ZomatoCloneApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('879x488')
        self.root.configure(background='#FFCCCC')  # Light red background for root
        self.root.title("Home window @Zomato clone")

        # Connect to MySQL database
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Tejeswar2006',
            database='zomato_clone'
        )
        print("Connected to MySQL database")

        # Create a frame to hold the elements
        self.frame = Frame(self.root, bg='#FFCCCC')  # Light red background for frame
        self.frame.pack(pady=20, fill=BOTH, expand=True)

        # This is the section of code which creates the label
        Label(self.frame, text='Zomato', bg='#FFCCCC', font=('arial', 40, 'normal')).pack(pady=(0, 10))

        # This is the section of code which creates a sub-frame for the search bar and label
        self.search_frame = Frame(self.frame, bg='#FFCCCC')  # Light red background for sub-frame
        self.search_frame.pack(pady=(0, 10))

        # This is the section of code which creates the label "Restaurants"
        Label(self.search_frame, text='Restaurants', bg='#FFCCCC', font=('arial', 20, 'normal')).pack(side=LEFT, padx=(0, 10))

        # This is the section of code which creates the search bar
        self.search_bar = Entry(self.search_frame, font=('arial', 20, 'normal'), width=30)
        self.search_bar.pack(side=LEFT, padx=(0, 10))

        # This is the section of code which creates the search button
        self.search_button = Button(self.search_frame, text='Search 🔎', bg='#F0F8FF', font=('arial', 15, 'normal'), command=self.search)
        self.search_button.pack(side=LEFT)

        # This is the section of code which creates a sub-frame for "Order Online" and "View History" buttons
        self.button_frame = Frame(self.frame, bg='#FFCCCC')
        self.button_frame.pack(pady=(20, 10))

        # This is the section of code which creates the "Order Online" button
        self.order_online_button = Button(self.button_frame, text='Order Online', bg='#F0F8FF', font=('arial', 15, 'normal'), command=self.display_top_restaurants)
        self.order_online_button.pack(side=LEFT, padx=10)

        # This is the section of code which creates the "View History" button
        self.view_history_button = Button(self.button_frame, text='View History', bg='#F0F8FF', font=('arial', 15, 'normal'), command=self.view_history)
        self.view_history_button.pack(side=LEFT, padx=10)

        # This is the section of code which creates the "YOU" button
        self.you_button = Button(self.root, text='YOU', bg='#F0F8FF', font=('arial', 15, 'normal'), command=self.you)
        self.you_button.place(relx=1.0, x=-10, y=10, anchor='ne')

        # Create a canvas widget and associate it with a scrollbar
        self.canvas = Canvas(self.frame, bg='#FFCCCC')
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(self.frame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Frame to display search results inside the canvas
        self.results_frame = Frame(self.canvas, bg='#FFCCCC')  # Light red background for frame
        self.results_frame_id = self.canvas.create_window((0, 0), window=self.results_frame, anchor='nw')

        # Configure resizing behavior
        self.frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Display top restaurants by default on startup
        self.display_top_restaurants()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.results_frame_id, width=event.width)

    def search(self):
        # Clear previous search results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        a = self.search_bar.get()
        c = self.conn.cursor()

        query = "SELECT * FROM restaurants WHERE name LIKE %s OR cuisine LIKE %s"  # Adjusted query
        c.execute(query, (a + '%', a + '%'))  # Pass both parameters
        results = c.fetchall()

        for restaurant in results:
            result_frame = Frame(self.results_frame, bg='#F0F8FF', padx=10, pady=10, relief=RAISED, bd=2)
            result_frame.pack(fill=X, pady=5, padx=20)

            # Container for restaurant name and additional info
            name_info_frame = Frame(result_frame, bg='#F0F8FF')
            name_info_frame.pack(side=LEFT, padx=(0, 10))

            # Restaurant name label
            name_label = Label(name_info_frame, text=restaurant[1], bg='#F0F8FF', font=('arial', 15, 'normal'))
            name_label.pack(side=TOP)

            # Additional information label (assuming this is the cuisine type, address, etc.)
            info_label = Label(name_info_frame, text=f"({restaurant[5]}) {restaurant[3]} - {restaurant[2]}", bg='#F0F8FF', font=('arial', 12, 'normal'))
            info_label.pack(side=TOP)

            # Rating label
            rating_label = Label(result_frame, text=f"{restaurant[4]} ⭐", bg='#F0F8FF', font=('arial', 15, 'normal'))
            rating_label.pack(side=RIGHT, padx=(10, 0))

            # Order button with restaurant ID
            order_button = Button(result_frame, text='View Menu', bg='#FF6666', font=('arial', 15, 'normal'), command=lambda r=restaurant: self.view_menu(r))
            order_button.pack(side=RIGHT, padx=(10, 10))

    def display_top_restaurants(self):
        # Clear previous top restaurant display
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Query top five restaurants by rating
        c = self.conn.cursor()
        query = "SELECT * FROM restaurants ORDER BY rating DESC LIMIT 5"
        c.execute(query)
        top_restaurants = c.fetchall()

        # Display top restaurants in a scrollable frame
        if top_restaurants:
            for idx, restaurant in enumerate(top_restaurants, start=1):
                result_frame = Frame(self.results_frame, bg='#F0F8FF', padx=10, pady=10, relief=RAISED, bd=2)
                result_frame.pack(fill=X, pady=5, padx=20)

                # Container for restaurant name and additional info
                name_info_frame = Frame(result_frame, bg='#F0F8FF')
                name_info_frame.pack(side=LEFT, padx=(0, 10))

                # Restaurant name label
                name_label = Label(name_info_frame, text=restaurant[1], bg='#F0F8FF', font=('arial', 15, 'normal'))
                name_label.pack(side=TOP)

                # Additional information label (assuming this is the cuisine type, address, etc.)
                info_label = Label(name_info_frame, text=f"({restaurant[5]}) {restaurant[3]} - {restaurant[2]}", bg='#F0F8FF', font=('arial', 12, 'normal'))
                info_label.pack(side=TOP)

                # Rating label
                rating_label = Label(result_frame, text=f"{restaurant[4]} ⭐", bg='#F0F8FF', font=('arial', 15, 'normal'))
                rating_label.pack(side=RIGHT, padx=(10, 0))

                # Order button with restaurant ID
                order_button = Button(result_frame, text='View Menu', bg='#FF6666', font=('arial', 15, 'normal'), command=lambda r=restaurant: self.view_menu(r))
                order_button.pack(side=RIGHT, padx=(10, 10))

        else:
            Label(self.results_frame, text="No restaurants found.", bg='#FFCCCC', font=('arial', 12, 'normal')).pack(pady=5)

        # Configure resizing behavior
        self.results_frame.update_idletasks()  # Update idle tasks to ensure proper sizing
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def view_menu(self, restaurant):
        # Create a new window for viewing the menu
        menu_window = Toplevel(self.root)
        menu_window.geometry('600x400')
        menu_window.configure(background='#FFCCCC')  # Light red background for menu window
        menu_window.title(f"Order food online in {restaurant[1]}")

        # Heading label
        Label(menu_window, text=f"Order food online in {restaurant[1]}", bg='#FFCCCC', font=('arial', 20, 'normal')).pack(pady=(10, 10))

        # Home button to close menu window and go back to previous window
        home_button = Button(menu_window, text='Home', bg='#FF6666', font=('arial', 15, 'normal'), command=menu_window.destroy)
        home_button.place(relx=1.0, x=-10, y=10, anchor='ne')

        # Create a canvas widget and associate it with a scrollbar
        canvas = Canvas(menu_window, bg='#FFCCCC')
        canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=(10, 0))

        scrollbar = Scrollbar(menu_window, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame to display menu items inside the canvas
        menu_frame = Frame(canvas, bg='#FFCCCC')
        menu_frame_id = canvas.create_window((0, 0), window=menu_frame, anchor='nw')

        c = self.conn.cursor()
        query = "SELECT * FROM menus WHERE restaurant_id = %s"
        c.execute(query, (restaurant[0],))
        menu_items = c.fetchall()

        # Display menu items
        for menu_item in menu_items:
            item_name = menu_item[2]
            item_price = menu_item[3]
            item_description = menu_item[4]  # Assuming description is in column index 4
            item_rating = menu_item[5]  # Assuming rating is in column index 5

            item_frame = Frame(menu_frame, bg='#F0F8FF', padx=10, pady=5, relief=RAISED, bd=1)
            item_frame.pack(fill=X, pady=5, padx=10)

            # Container for item name, order button, and rating
            item_container = Frame(item_frame, bg='#F0F8FF')
            item_container.pack(fill=X)

            # Item name label
            item_label = Label(item_container, text=item_name, bg='#F0F8FF', font=('arial', 12, 'normal'))
            item_label.pack(side=LEFT, padx=(10, 0))

            # Item price label
            item_price_label = Label(item_container, text=f'{item_price}$', bg='#F0F8FF', font=('arial', 12, 'normal'))
            item_price_label.pack(side=RIGHT, padx=(10, 0))

            # Order button
            order_button = Button(item_container, text='Order', bg='#FF6666', font=('arial', 12, 'normal'),command = lambda a=menu_item:self.order_(a))
            order_button.pack(side=RIGHT, padx=(10, 0))

            # Rating button
            def rate_item():
                # Function to handle rating
                rate_window = Toplevel(menu_window)
                rate_window.geometry('300x200')
                rate_window.title(f"Rate {item_name}")

                Label(rate_window, text=f"Rate {item_name}", font=('arial', 15, 'bold')).pack(pady=10)

                # Rating entry
                rating_entry = Entry(rate_window, font=('arial', 12))
                rating_entry.pack(pady=10)

                def submit_rating():
                    try:
                        rating = int(rating_entry.get())
                        if rating < 1 or rating > 5:
                            messagebox.showerror("Error", "Rating must be between 1 and 5")
                        else:
                            # Update database with the new rating
                            c = self.conn.cursor()
                            # 1. Fetch existing ratings
                            query = "SELECT total_rating, average_rating FROM menus WHERE menu_id = %s"
                            c.execute(query, (menu_item[0],))
                            result = c.fetchone()

                            if result:
                                total_ratings = result[0]
                                avg_rating = result[1]

                                # Calculate new average rating
                                new_total_ratings = total_ratings + 1
                                new_avg_rating = ((avg_rating * total_ratings) + rating) / new_total_ratings

                                # Update database with new values
                                update_query = "UPDATE menus SET total_rating = %s, average_rating = %s WHERE menu_id = %s"
                                c.execute(update_query, (new_total_ratings, new_avg_rating, menu_item[0]))
                                self.conn.commit()

                                # Provide feedback to the user
                                messagebox.showinfo("Success", f"Rated {item_name} with {rating} stars")
                                rate_window.destroy()

                                # Update the UI
                                rating_button.config(text=f"Rating: {new_avg_rating:.1f} ⭐")
                            else:
                                messagebox.showerror("Error", "Menu item not found in database.")

                    except ValueError:
                        messagebox.showerror("Error", "Invalid rating. Please enter a number.")

                # Submit button
                submit_button = Button(rate_window, text="Submit", command=submit_rating)
                submit_button.pack()

            rating_button = Button(item_container, text=f"Rating: {item_rating} ⭐", bg='#F0F8FF', font=('arial', 10, 'normal'), command=rate_item)
            rating_button.pack(side=RIGHT, padx=(10, 0))

            # Description label
            desc_label = Label(item_frame, text=item_description, bg='#F0F8FF', font=('arial', 10, 'italic'))
            desc_label.pack(fill=X, padx=(10, 0), pady=(5, 0))

        # Configure resizing behavior
        menu_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda event: canvas.itemconfig(menu_frame_id, width=event.width))

    def view_history(self):
        print('View History button clicked')

    def you(self):
        print('YOU button clicked')

    def order_(self,item):
        messagebox.showinfo("Order Status","Order Placed Successfully!!")
        

if __name__ == "__main__":
    root = Tk()
    app = ZomatoCloneApp(root)
    root.mainloop()