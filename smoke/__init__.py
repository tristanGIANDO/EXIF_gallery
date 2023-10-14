import sys
import os

package_path = os.path.dirname(os.path.dirname(__file__))
if package_path in sys.path:
    sys.path.remove(package_path)
sys.path.insert(0, package_path)