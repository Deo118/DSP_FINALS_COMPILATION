class NavigationManager:
    def __init__(self, views, sidebar):
        self.views = views
        self.sidebar = sidebar
        self.active_view = "dashboard"

    def initialize(self):
        self.views[self.active_view].pack(fill="both", expand=True)
        self.sidebar.activate(self.active_view)

    def switch_view(self, view_key):
        if view_key == self.active_view:
            return

        self.views[self.active_view].pack_forget()

        self.sidebar.deactivate(self.active_view)

        self.active_view = view_key

        self.views[self.active_view].pack(fill="both", expand=True)

        self.sidebar.activate(self.active_view)