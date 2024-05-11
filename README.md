# Basic Budget Financial Manager (BBFM)

BBFM is a financial management application that helps users track their bills, income, and distribute their money based on customizable scales. The application allows users to store their financial data, including bills, utilities, and paystubs, using JSON data storage.

## Features

- Add and manage bills (Payment Constants)
- Set and update utilities (Payment Fluctuations)
- Add paystubs and calculate money distribution
- View current finances and total money distribution
- Adjust distribution scales for different categories
- Reset bills, utilities, paystubs, and current finances

## Getting Started

### Prerequisites

- Python 3.11
- Kivy 2.3.0

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/Brycekratzer/Finance-App.git
   ```

2. Install the required dependencies:
   ```
   python -m pip install --upgrade pip setuptools virtualenv
   python -m venv kivy_venv
   source kivy_venv/bin/activate
   python -m pip install "kivy[base]" kivy_examples
   ```

### Running the Application

To run the application, execute the following command:
```
python ./src/main.py
```

## Usage

### Adding Bills

1. Navigate to the "Add/Edit Bills" page.
2. Enter the bill name and amount in the provided input fields.
3. Click the "Add Bill" button to save the bill.
4. To edit or delete a bill, use the corresponding buttons next to each bill entry.

### Setting Utilities

1. On the "Add/Edit Bills" page, locate the "Monthly Utility (Average)" section.
2. Enter the average cost of your utilities in the input field.
3. Click the "Update Utility" button to save the utility amount.

### Adding Paystubs

1. Go to the "Add pay stub" page.
2. If desired, click the "Adjust Distribution" button to modify the distribution scales before adding the paystub.
3. Enter the paystub amount in the input field.
4. Click the "Add Pay Stub" button to save the paystub and calculate the money distribution.

### Viewing Current Finances

1. Navigate to the "Current Finances" page.
2. The page displays the total money distributed to each finance category.
3. A bar graph shows the money distribution for each category compared to the total money earned for each paycheck.

### Adjusting Distributions

1. Go to the "Adjust Distributions" page.
2. Modify the distribution scales for each category using the provided sliders.
   - Aggressive distribution: 7-10
   - Moderate distribution: 4-6
   - Light distribution: 1-3
   - No funding: 0
3. Click the "Save Changes" button to apply the new distribution scales.
4. Based on predetermined calculations from the scale above, there are auto 
   recommend distributions given:
   - Debt: 8
   - Savings: 9
   - Lesiure: 2
   - Food: 5

### Resetting Data

1. On the main page, click the "Reset" button.
2. Choose the desired reset option:
   - Reset all paystubs and finances
   - Reset all bills and utilities
3. Confirm the reset action in the displayed popup.

## File Structure

- `main.py`: Main entry point for the application.
- `front_page.py`: FrontPage class representing the main page of the application.
- `ui_page.py`: UIPage class representing the user input page for managing bills and utilities.
- `aps_page.py`: APSPage class representing the add paystub page.
- `vcf_page.py`: VCFPage class representing the view current finances page.
- `ad_page.py`: ADPage class representing the adjust distributions page.
- `bills.json`: JSON file for storing bill data.
- `utility.json`: JSON file for storing utility data.
- `paystub.json`: JSON file for storing paystub data.
- `finance.json`: JSON file for storing current finance data.

## Calculations

The application performs the following calculations to distribute the money:

1. Total Bills (TB) = Total Payment Constants (TPC) / 2 + (Total Payment Fluctuations (TPF) * 1.1) / 2
2. Remaining Income (RI) = Paystub Amount - TB
3. Total Proportion = Debt Proportion + Savings Proportion + Leisure Proportion + Food Proportion
4. Debt Amount = (Debt Proportion / Total Proportion) × RI
5. Savings Amount = (Savings Proportion / Total Proportion) × RI
6. Leisure Amount = (Leisure Proportion / Total Proportion) × RI
7. Food Amount = (Food Proportion / Total Proportion) × RI

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

## Known Bugs
The program does not account for invalid inputs for bills, utilites, paystubs, and adjusting distributions.
## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [Kivy](https://kivy.org/) - Python framework for developing cross-platform applications
- [JsonStore](https://kivy.org/doc/stable/api-kivy.storage.html#kivy.storage.jsonstore.JsonStore) - Kivy's JSON storage module
