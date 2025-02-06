import importlib
import os, sys
from core.config_loader import config
from core.event_bus import event_bus

def load_modules():
    loaded_modules = {}

    for name, module_config in config.items():
        provider = module_config.get("provider")
        if provider:
            try:
                module_path = f"modules.{name}.{provider}"
                module = importlib.import_module(module_path)

                # Ensure each module defines a class named `Module`
                module_class = getattr(module, "Module", None)
                if module_class:
                    module_instance = module_class(module_config, event_bus)  # Pass event bus
                    loaded_modules[name] = module_instance
                    print(f"✅ Loaded module: {name} ({provider})")
                else:
                    print(f"⚠️ No `Module` class found in {module_path}, skipping.")

            except ModuleNotFoundError as e:
                print(f"⚠️ Module {module_path} not found, skipping: {e}")
            except Exception as e:
                print(f"⚠️ Error loading module {module_path}: {e}")

    return loaded_modules

modules = load_modules()