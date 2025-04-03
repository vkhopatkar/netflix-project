from PyQt5 import QtWidgets
from PyQt5 import QtWidgets, QtCore, QtGui 
from ui.netflix_ui import Ui_NetflixExplorer
import pandas as pd

class NetflixApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_NetflixExplorer()
        self.ui.setupUi(self)
        self.df = pd.read_csv(r"E:\git_projects\netflix_titles (WIP)\netflix_data\netflix_data.csv").fillna("")
        print(self.df.head())  # Debugging line to check if the DataFrame is loaded correctly

        self.ui.genre_combobox.addItem("All")
        self.ui.country_combobox.addItem("All")
        genres = sorted(set(self.df['listed_in'].dropna().str.split(', ').sum()))
        countries = sorted(set(self.df['country'].dropna().str.split(', ').sum()))
        self.ui.genre_combobox.addItems(genres)
        self.ui.country_combobox.addItems(countries)
        self.apply_filters()
        self.ui.filter_botton.clicked.connect(self.apply_filters)

    def apply_filters(self):
        df = self.df.copy()

        title = self.ui.searchbar.text().strip().lower()
        genre = self.ui.genre_combobox.currentText()
        country = self.ui.country_combobox.currentText()

        print(f"Title: {title}, Genre: {genre}, Country: {country}")  # Debugging line

        # Clean missing data
        df['title'] = df['title'].fillna("").astype(str)
        df['listed_in'] = df['listed_in'].fillna("").astype(str)
        df['country'] = df['country'].fillna("").astype(str)

        # Filter by title
        if title:
            df = df[df['title'].str.lower().str.contains(title, na=False)]
        else:
            print("No title filter applied")

        # Filter by genre
        if genre != "All":
            df = df[df['listed_in'].str.contains(genre, case=False, na=False)]
        else:
            print("No genre filter applied")

        # Filter by country
        if country != "All":
            df = df[df['country'].str.contains(country, case=False, na=False)]
        else:
            print("No country filter applied")

        print("Filtered rows:", len(df))
        self.display_results(df)

    def display_results(self, df):
        table = self.ui.output_table
        df = df.fillna("")

        row_count = len(df)
        print(f"\n Displaying {row_count} results...\n")

        table.clearContents()
        table.setRowCount(row_count)
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Title", "Type", "Release Year", "Rating", "Duration"])

        for display_row, (_, row) in enumerate(df.iterrows()):
            title = str(row.get('title', '') or "N/A").strip()
            type_ = str(row.get('type', '') or "N/A").strip()
            year = str(row.get('release_year', '') or "N/A").strip()
            rating = str(row.get('rating', '') or "N/A").strip()
            duration = str(row.get('duration', '')).strip() or "N/A"

            print(f"Row {display_row+1} → Title: {title}, Type: {type_}, Year: {year}, Rating: {rating}, Duration: {duration}")

            title_item = QtWidgets.QTableWidgetItem(title)
            type_item = QtWidgets.QTableWidgetItem(type_)
            year_item = QtWidgets.QTableWidgetItem(year)
            rating_item = QtWidgets.QTableWidgetItem(rating)
            duration_item = QtWidgets.QTableWidgetItem(duration)

            # Highlight missing duration
            if duration == "N/A":
                duration_item.setForeground(QtGui.QBrush(QtGui.QColor("red")))
                font = duration_item.font()
                font.setItalic(True)
                duration_item.setFont(font)

            for item in [title_item, type_item, year_item, rating_item, duration_item]:
                item.setTextAlignment(QtCore.Qt.AlignCenter)

            table.setItem(display_row, 0, title_item)
            table.setItem(display_row, 1, type_item)
            table.setItem(display_row, 2, year_item)
            table.setItem(display_row, 3, rating_item)
            table.setItem(display_row, 4, duration_item)

        table.resizeColumnsToContents()
        table.scrollToTop()

        if row_count == 0:
            print(" No results found for the current filter.\n")
        else:
            print(" Results successfully loaded into the table.\n")



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = NetflixApp()
    window.show()
    sys.exit(app.exec_())
