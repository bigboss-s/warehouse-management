from warehouse.warehouse_app import WarehouseApp

if __name__ == "__main__":
    app = WarehouseApp('Warehouse')
    app.mainloop()
    app.db.close()
