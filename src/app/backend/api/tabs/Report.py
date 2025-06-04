    
from django.conf import settings
from django.http import JsonResponse, HttpResponse
import requests
import json
import os
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from api.constants import REPORT_TEMPLATE_PATH

INVOICE_NINJA_API_URL = settings.INVOICE_NINJA_API_URL
INVOICE_NINJA_API_TOKEN = settings.INVOICE_NINJA_API_TOKEN
MEDIA_ROOT = settings.MEDIA_ROOT


class Report:
    def __init__(self):
        self.report_dir = '/home/suyash/Downloads/Reports'
        # Create the reports directory if it doesn't exist
        os.makedirs(self.report_dir, exist_ok=True)
    
    def appropriate_function(self, transcript=None, json_input=None):
        """
        Process either transcript through LLM or direct JSON input
        """
        if transcript:
            with open(REPORT_TEMPLATE_PATH) as f:
                prompt = f.read()

            prompt += f""" Now extract from: '{transcript}' """

            OLLAMA_URL = "http://localhost:11434/api/generate"

            data = {
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }

            response = requests.post(OLLAMA_URL, json=data)
            if response.status_code == 200:
                response_string = response.json().get("response", "").strip()
                try:
                    json_output = json.loads(response_string)
                except json.JSONDecodeError:
                    print(f"Failed to parse JSON: {response_string}")
                    return JsonResponse({"status": "error", "message": "Failed to parse LLM response"})
            else:
                print(f"API request failed with status code: {response.status_code}")
                return JsonResponse({"status": "error", "message": "API request failed"})
        elif json_input:
            # Use the provided JSON directly
            json_output = json_input
        else:
            return JsonResponse({"status": "error", "message": "Either transcript or json_input must be provided"})
        
        # Debug logs
        print(f"The json_output is {json_output}")
                                                    
        operation = json_output.get("operation", "").strip().lower()
        product_ids = json_output.get("product_ids", [])
        
        print(f"Operation: {operation}")
        print(f"Product IDs: {product_ids}")
        
        if operation == "profit_loss":
            return self.generate_profit_loss_report(product_ids)
        
        if operation == "sales_report":
            # You can implement sales report functionality here
            return self.generate_loans_report()
        
        return JsonResponse({"status": "Client appropriate function called"})

    def create_chart(self, df, chart_type='profit_by_product'):
    
        plt.figure(figsize=(10, 6))
        
        if chart_type == 'profit_by_product':
            # Group by product ID and calculate profit
            profit_by_product = df.groupby('soldProductId')['profit'].sum()
            
            plt.bar(profit_by_product.index.astype(str), profit_by_product.values)
            plt.title('Profit by Product ID')
            plt.xlabel('Product ID')
            plt.ylabel('Profit (Rs)')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
        elif chart_type == 'profit_margin':
            # Group by product ID and calculate average profit margin
            margin_by_product = df.groupby('soldProductId')['profit_margin'].mean()
            
            plt.bar(margin_by_product.index.astype(str), margin_by_product.values)
            plt.title('Profit Margin by Product ID')
            plt.xlabel('Product ID')
            plt.ylabel('Profit Margin (%)')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
        # Save the chart to a BytesIO object
        img_data = BytesIO()
        plt.savefig(img_data, format='png')
        img_data.seek(0)
        plt.close()
        
        return img_data        # Test code to handle the example in the error output

    def generate_profit_loss_report(self, product_ids):
        # Fetch sales data
        response = requests.get('http://localhost:8080/api/db/product/sell')
        
        if response.status_code != 200:
            return JsonResponse({"status": "error", "message": "Failed to fetch sales data"})
            
        sales_data = response.json()
        
        # Debug logs
        print("Inside profit_loss")
        print(f"All sales data: {sales_data}")
        print(f"Product IDs to filter: {product_ids}")
        
        # Convert product_ids to integers for comparison
        # Some might be strings from the LLM response
        product_ids_int = []
        for pid in product_ids:
            try:
                product_ids_int.append(int(pid))
            except (ValueError, TypeError):
                # If conversion fails, keep the original value
                product_ids_int.append(pid)
        
        # Filter data based on product_ids if provided
        filtered_data = []
        if product_ids_int:
            for item in sales_data:
                # Handle different data types by converting to the same type
                sold_product_id = item.get('soldProductId')
                if isinstance(sold_product_id, str) and sold_product_id.isdigit():
                    sold_product_id = int(sold_product_id)
                
                if sold_product_id in product_ids_int:
                    filtered_data.append(item)
        else:
            filtered_data = sales_data
        
        print(f"Filtered data: {filtered_data}")
            
        if not filtered_data:
            return JsonResponse({
                "status": "warning", 
                "message": "No matching products found",
                "product_ids_requested": product_ids,
                "all_available_ids": [item.get('soldProductId') for item in sales_data]
            })
            
        # Convert to pandas DataFrame for easier processing
        df = pd.DataFrame(filtered_data)
        
        # Calculate profit metrics
        df['cost'] = df['soldProductActualPrice'].astype(float) * df['soldProductQuantity'].astype(float)
        df['revenue'] = df['soldProductSellingPrice'].astype(float) * df['soldProductQuantity'].astype(float)
        df['profit'] = df['revenue'] - df['cost']
        df['profit_margin'] = (df['profit'] / df['revenue']) * 100
        
        # Generate PDF report
        report_path = self.create_profit_loss_pdf(df)
        
        return JsonResponse({
            "status": "success", 
            "message": "Profit and loss report generated successfully",
            "report_url": report_path
        })
    
    def generate_loans_report(self):
        """Generate a loans report with detailed information about loans and transactions"""
        # Fetch loans data
        loans_response = requests.get('http://localhost:8080/api/db/loans/list')
        if loans_response.status_code != 200:
            return JsonResponse({"status": "error", "message": "Failed to fetch loans data"})
        
        loans_data = loans_response.json()
        print(f"Loans data: {loans_data}")
        
        # Fetch transactions data
        transactions_response = requests.get('http://localhost:8080/api/db/transactions/list')
        if transactions_response.status_code != 200:
            return JsonResponse({"status": "error", "message": "Failed to fetch transactions data"})
        
        transactions_data = transactions_response.json()
        print(f"Transactions data: {transactions_data}")
        
        # Process data
        if not loans_data:
            return JsonResponse({"status": "warning", "message": "No loans data found"})
        
        # Create pandas DataFrames for easier data manipulation
        loans_df = pd.DataFrame(loans_data)
        transactions_df = pd.DataFrame(transactions_data)
        
        # Generate PDF report
        report_path = self.create_loans_pdf(loans_df, transactions_df)
        
        return JsonResponse({
            "status": "success", 
            "message": "Loans report generated successfully",
            "report_url": report_path
        })
        
    def create_loans_pdf(self, loans_df, transactions_df):
        """Generate a PDF report for loans"""
        # Create a filename with current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"loans_report_{timestamp}.pdf"
        filepath = os.path.join(self.report_dir, filename)
        
        # Create the PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Add title
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=18,
            alignment=1,
            spaceAfter=12
        )
        elements.append(Paragraph("Loans Report", title_style))
        elements.append(Spacer(1, 0.25*inch))
        
        # Add date
        date_style = ParagraphStyle(
            'Date', 
            parent=styles['Normal'],
            fontSize=10,
            alignment=1
        )
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", date_style))
        elements.append(Spacer(1, 0.5*inch))
        
        # Summary section
        elements.append(Paragraph("Loans Summary", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        # Calculate summary metrics
        total_loan_amount = loans_df['loanAmount'].astype(float).sum()
        num_borrowers = loans_df['personName'].nunique()
        avg_loan_amount = total_loan_amount / num_borrowers if num_borrowers > 0 else 0
        
        # Create summary table
        summary_data = [
            ["Metric", "Value"],
            ["Total Outstanding Loans", f"Rs{total_loan_amount:.2f}"],
            ["Number of Borrowers", str(num_borrowers)],
            ["Average Loan Amount", f"Rs{avg_loan_amount:.2f}"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (1, 0), 12),
            ('BACKGROUND', (0, 1), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Add loan distribution chart
        elements.append(Paragraph("Loan Distribution by Person", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        # Create loan distribution chart
        loan_chart = self.create_loan_chart(loans_df)
        img = Image(loan_chart, width=6*inch, height=3*inch)
        elements.append(img)
        elements.append(Spacer(1, 0.3*inch))
        
        # Detailed loans section
        elements.append(Paragraph("Outstanding Loans", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        # Create table for detailed loans data
        loans_table_data = [
            ["Person Name", "Email", "Amount", "Description"]
        ]
        
        for _, row in loans_df.iterrows():
            email = row.get('email', '')
            if pd.isna(email) or email is None:
                email = 'N/A'
                
            description = row.get('description', '')
            if pd.isna(description) or description is None:
                description = 'N/A'
            else:
                # Truncate description if it's too long
                description = description[:50] + '...' if len(description) > 50 else description
                
            loans_table_data.append([
                str(row['personName']),
                str(email),
                f"Rs{float(row['loanAmount']):.2f}",
                str(description)
            ])
        
        loans_table = Table(loans_table_data, colWidths=[1.5*inch, 2*inch, 1*inch, 2.5*inch])
        loans_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
        ]))
        elements.append(loans_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Transactions section
        if not transactions_df.empty:
            elements.append(Paragraph("Recent Transactions", styles['Heading2']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Create transaction type distribution chart
            transaction_chart = self.create_transaction_chart(transactions_df)
            img = Image(transaction_chart, width=6*inch, height=3*inch)
            elements.append(img)
            elements.append(Spacer(1, 0.3*inch))
            
            # Create table for transaction data
            transactions_table_data = [
                ["ID", "Person", "Type", "Amount", "Description"]
            ]
            
            # Sort transactions by ID (most recent first)
            sorted_transactions = transactions_df.sort_values(by='id', ascending=False)
            
            # Take only the last 10 transactions to avoid a very long report
            last_transactions = sorted_transactions.head(10)
            
            for _, row in last_transactions.iterrows():
                description = row.get('description', '')
                if pd.isna(description) or description is None or description == '':
                    description = 'N/A'
                    
                loan_type = row.get('loanType', '')
                if pd.isna(loan_type) or loan_type is None:
                    loan_type = 'N/A'
                    
                transactions_table_data.append([
                    str(row['id']),
                    str(row['personName']),
                    str(loan_type),
                    f"Rs{float(row['loanAmount']):.2f}",
                    str(description)
                ])
            
            transactions_table = Table(transactions_table_data, colWidths=[0.5*inch, 1.5*inch, 1*inch, 1*inch, 3*inch])
            transactions_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
            ]))
            elements.append(transactions_table)
        
        # Build the PDF
        doc.build(elements)
        
        # Return path to the report file
        return filepath
        
    def create_loan_chart(self, loans_df):
        """Create a pie chart showing loan distribution by person"""
        plt.figure(figsize=(10, 6))
        
        # Group by person and sum loan amounts
        loan_by_person = loans_df.groupby('personName')['loanAmount'].sum()
        
        # Create pie chart
        plt.pie(loan_by_person.values, labels=loan_by_person.index, autopct='%1.1f%%', 
                shadow=True, startangle=90)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title('Loan Distribution by Person')
        plt.tight_layout()
        
        # Save the chart to a BytesIO object
        img_data = BytesIO()
        plt.savefig(img_data, format='png')
        img_data.seek(0)
        plt.close()
        
        return img_data
        
    def create_transaction_chart(self, transactions_df):
        """Create a chart showing transaction types"""
        plt.figure(figsize=(10, 6))
        
        # Count transaction types
        transaction_types = transactions_df['loanType'].value_counts()
        
        # Create bar chart
        plt.bar(transaction_types.index, transaction_types.values)
        plt.title('Transaction Types')
        plt.xlabel('Transaction Type')
        plt.ylabel('Count')
        plt.tight_layout()
        
        # Save the chart to a BytesIO object
        img_data = BytesIO()
        plt.savefig(img_data, format='png')
        img_data.seek(0)
        plt.close()
        
        return img_data
        
    def create_profit_loss_pdf(self, df):
        """Generate a PDF report for profit and loss"""
        # Create a filename with current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"profit_loss_report_{timestamp}.pdf"
        filepath = os.path.join(self.report_dir, filename)
        
        # Create the PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Add title
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=18,
            alignment=1,
            spaceAfter=12
        )
        elements.append(Paragraph("Profit and Loss Report", title_style))
        elements.append(Spacer(1, 0.25*inch))
        
        # Add date
        date_style = ParagraphStyle(
            'Date', 
            parent=styles['Normal'],
            fontSize=10,
            alignment=1
        )
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", date_style))
        elements.append(Spacer(1, 0.5*inch))
        
        # Summary section
        elements.append(Paragraph("Summary", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        # Calculate summary metrics
        total_cost = df['cost'].sum()
        total_revenue = df['revenue'].sum()
        total_profit = df['profit'].sum()
        avg_margin = df['profit_margin'].mean()
        
        # Create summary table
        summary_data = [
            ["Metric", "Value"],
            ["Total Cost", f"Rs{total_cost:.2f}"],
            ["Total Revenue", f"Rs{total_revenue:.2f}"],
            ["Total Profit", f"Rs{total_profit:.2f}"],
            ["Average Profit Margin", f"{avg_margin:.2f}%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (1, 0), 12),
            ('BACKGROUND', (0, 1), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Add profit chart
        elements.append(Paragraph("Profit by Product", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        profit_chart = self.create_chart(df, 'profit_by_product')
        img = Image(profit_chart, width=6*inch, height=3*inch)
        elements.append(img)
        elements.append(Spacer(1, 0.3*inch))
        
        # Add margin chart
        elements.append(Paragraph("Profit Margin by Product", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        margin_chart = self.create_chart(df, 'profit_margin')
        img = Image(margin_chart, width=6*inch, height=3*inch)
        elements.append(img)
        elements.append(Spacer(1, 0.3*inch))
        
        # Detailed data section
        elements.append(Paragraph("Detailed Data", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        # Create table for detailed data
        # Select and reformat the columns we want to show
        table_data = [
            ["Product ID", "Qty", "Cost Price", "Selling Price", "Revenue", "Profit", "Margin (%)"]
        ]
        
        for _, row in df.iterrows():
            table_data.append([
                str(row['soldProductId']),
                str(int(row['soldProductQuantity'])),
                f"Rs{float(row['soldProductActualPrice']):.2f}",
                f"Rs{float(row['soldProductSellingPrice']):.2f}",
                f"Rs{row['revenue']:.2f}",
                f"Rs{row['profit']:.2f}",
                f"{row['profit_margin']:.2f}%"
            ])
        
        detail_table = Table(table_data, colWidths=[0.7*inch, 0.5*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1*inch])
        detail_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ]))
        elements.append(detail_table)
        
        # Build the PDF
        doc.build(elements)
        
        # Return path to the report file
        return filepath
