except Exception as e:
            err_msg = str(e)   # capture message safely
            set_status("Error")
            root.after(0, lambda msg=err_msg: messagebox.showerror("Download Failed", msg))