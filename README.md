# ADK Project

A comprehensive business management system built with Python, featuring a modern web UI for sales tracking and a multi-tool agent for weather and time queries.

## Project Overview

This project consists of three main components:

1. **UI App** - A modern web application built with Reflex for business data management
2. **Multi-Tool Agent** - An AI agent using Google ADK for weather and time queries
3. **Data Analysis** - Jupyter notebook for data injection and PostgreSQL database operations

## Features

### 🌐 Web Application (UI App)
- **Modern Dashboard**: Interactive overview with charts and statistics
- **Product Management**: Add, edit, and track products with pricing
- **Sales Tracking**: Record and monitor sales transactions
- **Database Integration**: PostgreSQL backend for data persistence
- **Responsive Design**: Clean, modern interface built with Reflex
- **Data Visualization**: Charts and graphs for business insights

### 🤖 Multi-Tool Agent
- **Weather Reports**: Get current weather information for cities
- **Time Queries**: Retrieve current time for different locations
- **AI-Powered**: Uses Google ADK with Gemini 2.0 Flash model
- **Extensible**: Easy to add new tools and capabilities

### 📊 Data Management
- **Database Operations**: PostgreSQL integration for data storage
- **Data Injection**: Jupyter notebook for batch data operations
- **Category Management**: Expense category tracking
- **CSV Data Import**: Support for importing business data

## Tech Stack

- **Frontend**: Reflex (Python-based web framework)
- **Backend**: SQLAlchemy, PostgreSQL
- **AI/ML**: Google ADK, Gemini 2.0 Flash
- **Data Analysis**: Pandas, Jupyter Notebook
- **Database**: PostgreSQL with psycopg2

## Prerequisites

- Python 3.10+
- PostgreSQL database
- Google ADK access (for agent functionality)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ADK
   ```

2. **Set up the web application**
   ```bash
   cd ui_app
   pip install -r requirements.txt
   ```

3. **Configure database**
   Create a `.env` file in the `ui_app` directory:
   ```env
   DATABASE_URL=postgresql://postgres:123456@localhost:5433/postgres
   ```

4. **Initialize the database**
   Make sure PostgreSQL is running and create the necessary tables:
   ```python
   # Run this in Python or add to your startup script
   from ui_app.backend.database import engine, Base
   Base.metadata.create_all(bind=engine)
   ```

## Usage

### Running the Web Application

```bash
cd ui_app
reflex run
```

The application will be available at `http://localhost:3000`

### Using the Multi-Tool Agent

```python
from multi_tool_agent.agent import root_agent

# Get weather information
weather_response = root_agent.query("What's the weather like in New York?")

# Get current time
time_response = root_agent.query("What time is it in New York?")
```

### Data Analysis

Open the `inject.ipynb` notebook to:
- Connect to the PostgreSQL database
- Import product data
- Perform data analysis operations
- Generate reports

## Project Structure

```
ADK/
├── ui_app/                     # Web application
│   ├── ui_app/
│   │   ├── backend/           # Database models and operations
│   │   ├── components/        # UI components
│   │   ├── pages/            # Application pages
│   │   ├── templates/        # Page templates
│   │   └── views/            # View components and charts
│   ├── assets/               # Static assets
│   └── requirements.txt      # Python dependencies
├── multi_tool_agent/         # AI agent
│   ├── agent.py             # Main agent implementation
│   └── __init__.py
├── data/                    # Data files
│   └── kategori_pengeluaran.csv
├── inject.ipynb            # Data analysis notebook
└── README.md
```

## Database Schema

### Products Table (produk)
- `id_produk`: Primary key
- `nama_produk`: Product name
- `harga_produk`: Product price

### Sales Table (penjualan)
- `id_penjualan`: Primary key
- `id_produk`: Foreign key to products
- `kuantitas`: Quantity sold
- `harga_saat_penjualan`: Price at time of sale
- `total`: Computed total (quantity × price)
- `catatan`: Notes
- `tanggal_penjualan`: Sale date

## Configuration

### Environment Variables

Create a `.env` file in the `ui_app` directory:

```env
DATABASE_URL=postgresql://username:password@localhost:port/database_name
```

### Database Connection

Default connection settings:
- Host: localhost
- Port: 5433
- Database: postgres
- Username: postgres
- Password: 123456

## Development

### Adding New Features

1. **Web Application**: Add new pages in `ui_app/pages/` and components in `ui_app/components/`
2. **Agent Tools**: Add new functions to `multi_tool_agent/agent.py` and register them with the agent
3. **Database Models**: Extend models in `ui_app/backend/database.py`

### Testing

Run the application in development mode:
```bash
cd ui_app
reflex run --env dev
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed information

## Roadmap

- [ ] Add user authentication
- [ ] Implement advanced analytics
- [ ] Add more agent tools
- [ ] Mobile app development
- [ ] API documentation
- [ ] Unit tests
- [ ] Docker containerization