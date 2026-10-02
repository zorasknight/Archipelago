import asyncio
import json
import logging

tracker_loaded = False

try:
    from worlds.tracker.TrackerClient import ( TrackerGameContext as SuperContext, TrackerCommandProcessor as SuperCommandProcessor, )

    tracker_loaded = True

except ModuleNotFoundError:
    from CommonClient import ( CommonContext as SuperContext, ClientCommandProcessor as SuperCommandProcessor, )

from CommonClient import ( server_loop, gui_enabled, get_base_parser, )


class YakuzaGaidenContext(SuperContext):
    game = "Yakuza Gaiden"

    def make_gui(self):
        base_manager = super().make_gui()

        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.label import Label

        class YakuzaGaidenManager(base_manager):
            logging_pairs = [ ("Client", "Archipelago") ]

            base_title = "Archipelago Yakuza Gaiden Client"

            def select_randomizer_folder(self, _button):
                try:
                    from .randomizer import ( select_folder, folder_is_valid, )

                    folder = select_folder( self.set_randomizer_status )

                    if folder:
                        self.randomizer_folder = folder
                        self.randomizer_path.text = str(folder)

                        if folder_is_valid(folder):
                            self.randomizer_status.text = "Randomizer folder found."
                            self.run_button.disabled = False
                        else:
                            self.randomizer_status.text = "Randomizer folder needs to be created."
                            self.run_button.disabled = True

                except Exception as e:
                    self.randomizer_status.text = f"Error: {e}"

                    logging.getLogger("Client").exception( "Failed to select randomizer folder." )

            def set_randomizer_status(self, message):
                self.randomizer_status.text = message
                logging.getLogger("Client").info(message)

            def create_randomizer_folder(self, _button):
                try:
                    from .randomizer import ( create_folder_layout, folder_is_valid, )

                    folder = self.randomizer_folder

                    if not folder:
                        self.randomizer_status.text = "Please select a folder first."
                        return

                    create_folder_layout( self.set_randomizer_status, folder, )

                    if folder_is_valid(folder):
                        self.randomizer_status.text = "Randomizer folder found."
                        self.run_button.disabled = False
                    else:
                        self.randomizer_status.text = "Randomizer folder needs to be created."
                        self.run_button.disabled = True

                except Exception as e:
                    self.randomizer_status.text = f"Error: {e}"

                    logging.getLogger("Client").exception( "Failed to create randomizer folder." )

            def run_randomizer(self, _button):
                try:
                    from .randomizer import run_randomizer

                    folder = self.randomizer_folder

                    if not folder:
                        self.randomizer_status.text = "Please select a folder first."
                        return

                    run_randomizer( self.set_randomizer_status, folder, )

                except Exception as e:
                    self.randomizer_status.text = f"Error: {e}"

                    logging.getLogger("Client").exception( "Failed to run randomizer." )

            def build(self):
                root = super().build()
                self.randomizer_folder = None

                layout = BoxLayout( orientation="vertical", padding=10, spacing=10, )

                folder_row = BoxLayout( orientation="horizontal", size_hint_y=None, height=50, spacing=10, )

                select_button = Button( text="Select Folder Location", size_hint_x=None, width=200, on_release=lambda button: self.select_randomizer_folder(button), )

                self.randomizer_status = Label( text="Randomizer folder not created.", size_hint_y=None, height=40, )

                self.randomizer_path = Label( text="No folder selected.", )

                create_button = Button( text="Create Randomizer Folder", size_hint_y=None, height=50, on_release=lambda button: self.create_randomizer_folder(button), )

                self.run_button = Button( text="Run Randomizer", size_hint_y=None, height=50, disabled=True, on_release=lambda button: self.run_randomizer(button), )

                from .randomizer import ( load_saved_folder, folder_is_valid, )

                self.randomizer_folder = load_saved_folder()

                if self.randomizer_folder:
                    self.randomizer_path.text = str(self.randomizer_folder)

                    if folder_is_valid(self.randomizer_folder):
                        self.randomizer_status.text = "Randomizer folder found."
                        self.run_button.disabled = False
                    else:
                        self.randomizer_status.text = "Randomizer folder needs to be created."
                        self.run_button.disabled = True

                folder_row.add_widget(select_button)
                folder_row.add_widget(self.randomizer_path)

                layout.add_widget(folder_row)
                layout.add_widget(self.randomizer_status)
                layout.add_widget(create_button)
                layout.add_widget(self.run_button)

                self.add_client_tab( "Randomizer", layout, )

                return root

        return YakuzaGaidenManager

async def handle_status_client(reader, writer):
    #handles connection to main Yak client, only one way for now, will it be helpful to have it work the other way?
    try:
        command = await reader.readline()

        if command.decode().strip().upper() != "STATUS":
            writer.write(b'{"error":"unknown command"}\n')
            await writer.drain()
            return

        ctx = handle_status_client.ctx

        server = ctx.server_address

        if server and "@" in server:
            server = server.split("@", 1)[1]

        if server and server.startswith("wss://"):
            server = server[6:]

        response = {
            "connected": ctx.server is not None,
            "server": server,
            "slot": getattr(ctx, "auth", None),
            "password": "" if ctx.password in (None, "None") else ctx.password,
        }

        writer.write( (json.dumps(response) + "\n").encode("utf-8") )

        await writer.drain()

    finally:
        writer.close()
        await writer.wait_closed()

def launch():
    async def main(args):
        ctx = YakuzaGaidenContext( args.connect, args.password, )

        status_server = await asyncio.start_server( handle_status_client, "127.0.0.1", 38282, )

        handle_status_client.ctx = ctx

        ctx.server_task = asyncio.create_task( server_loop(ctx), name="server loop", )

        if tracker_loaded:
            ctx.run_generator()

        if gui_enabled:
            ctx.run_gui()

        ctx.run_cli()

        await ctx.exit_event.wait()

        status_server.close()
        await status_server.wait_closed()

        ctx.server_address = None

        await ctx.shutdown()

    parser = get_base_parser( description="Yakuza Gaiden Client, AP edition." )

    args, rest = parser.parse_known_args()

    asyncio.run(main(args))