import importlib
from core.config_loader import config
from core.event_bus import event_bus

def load_modules(event_bus):
    loaded_modules = {}
    pending_modules = {}

    # First, load all modules that have no dependencies
    for name, module_config in config.items():
        provider = module_config.get("provider")
        dependencies = module_config.get("dependencies", [])

        if dependencies:
            pending_modules[name] = {"config": module_config, "dependencies": dependencies}
        else:
            try:
                module = importlib.import_module(f"modules.{name}.{provider}")
                loaded_modules[name] = module.Module(module_config, event_bus)
                print(f"✅ Loaded module: {name}")
            except ModuleNotFoundError:
                print(f"⚠️ Module {name} not found, skipping.")

    # Now load modules that have dependencies
    while pending_modules:
        to_remove = []
        for name, module_info in pending_modules.items():
            dependencies_met = all(dep in loaded_modules for dep in module_info["dependencies"])

            if dependencies_met:
                provider = module_info["config"]["provider"]
                try:
                    module = importlib.import_module(f"modules.{name}.{provider}")
                    loaded_modules[name] = module.Module(module_info["config"], event_bus, loaded_modules)
                    print(f"✅ Loaded modulex: {name}")
                    to_remove.append(name)  # Mark module for removal
                except ModuleNotFoundError:
                    print(f"⚠️ Module {name} not found, skipping.")

        # Remove loaded modules from pending list
        for name in to_remove:
            del pending_modules[name]

        if not to_remove:
            print("⚠️ Circular dependency detected! Check module configurations.")
            break

    return loaded_modules

modules = load_modules(event_bus)