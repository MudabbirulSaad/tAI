#!/bin/bash
set -e

# Default to version 1.0.0 if no argument is provided
VERSION=${1:-1.0.0}
PACKAGE_NAME="tai"
DEB_FILE="${PACKAGE_NAME}_${VERSION}.deb"

echo "--- Starting installation for $PACKAGE_NAME version $VERSION ---"

# 1. Run the setup script to build the .deb package
echo "--- Building the package... ---"
bash setup.bash "$VERSION"

if [ ! -f "$DEB_FILE" ]; then
    echo "❌ Error: Build failed. Debian package file '$DEB_FILE' not found."
    exit 1
fi

# 2. Install the .deb package
echo "--- Installing the Debian package ($DEB_FILE)... ---"
sudo apt install -y "./$DEB_FILE"

# 3. Clean up the .deb file after successful installation
echo "--- Cleaning up the .deb file... ---"
rm "$DEB_FILE"

echo "✅ --- $PACKAGE_NAME version $VERSION has been successfully installed. ---" 