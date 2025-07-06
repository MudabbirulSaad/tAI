#!/bin/bash
set -e

# Default to version 1.0.0 if no argument is provided
VERSION=${1:-1.0.0}
PACKAGE_NAME="tai"
BUILD_DIR="${PACKAGE_NAME}-package-builder"

echo "--- Starting build for $PACKAGE_NAME version $VERSION ---"

# 1. Clean up previous build artifacts
echo "--- Cleaning up previous builds ---"
rm -rf "$BUILD_DIR"
rm -f "${PACKAGE_NAME}_${VERSION}_all.deb"
rm -f "${BUILD_DIR}.deb"

# Ensure a .env file exists so it can be bundled
if [ ! -f .env ]; then
    echo "--- .env file not found, creating empty one ---"
    touch .env
fi

# 2. Create the Debian package file structure
echo "--- Creating package structure ---"
mkdir -p "$BUILD_DIR/DEBIAN"
mkdir -p "$BUILD_DIR/usr/local/bin"
mkdir -p "$BUILD_DIR/usr/local/lib/$PACKAGE_NAME"

# 3. Copy source code to the target directory
echo "--- Copying source code ---"
rsync -av --progress . "$BUILD_DIR/usr/local/lib/$PACKAGE_NAME/" \
    --exclude ".git" \
    --exclude "venv" \
    --exclude "*package-builder" \
    --exclude ".idea" \
    --exclude "__pycache__" \
    --exclude "*.pyc" \
    --exclude "setup.bash"

# 4. Create a virtual environment inside the package structure
echo "--- Creating virtual environment ---"
python3 -m venv "$BUILD_DIR/usr/local/lib/$PACKAGE_NAME/venv"

# 5. Install dependencies from requirements.txt into the venv
echo "--- Installing dependencies ---"
"$BUILD_DIR/usr/local/lib/$PACKAGE_NAME/venv/bin/python3" -m pip install -r "$BUILD_DIR/usr/local/lib/$PACKAGE_NAME/requirements.txt"

# 6. Create the launcher script
echo "--- Creating launcher script ---"
cat <<EOF > "$BUILD_DIR/usr/local/bin/$PACKAGE_NAME"
#!/bin/sh
# Use exec to replace the shell process with the Python process
# This executes the python from your bundled venv, running your main script
# "\$@" passes along any command-line arguments to your application
exec /usr/local/lib/$PACKAGE_NAME/venv/bin/python3 /usr/local/lib/$PACKAGE_NAME/main.py "\$@"
EOF

# 7. Make the launcher script executable
echo "--- Making launcher executable ---"
chmod +x "$BUILD_DIR/usr/local/bin/$PACKAGE_NAME"

# 8. Create the control file for the Debian package
echo "--- Creating control file ---"
cat <<EOF > "$BUILD_DIR/DEBIAN/control"
Package: $PACKAGE_NAME
Version: $VERSION
Architecture: all
Maintainer: Shoaib <shoaib@gmail.com>
Description: tai is a tool that helps you to find the right command.
Depends: python3, python3-venv
EOF

# 9. Create post-installation script to set permissions
echo "--- Creating postinst script ---"
cat <<EOF > "$BUILD_DIR/DEBIAN/postinst"
#!/bin/sh
set -e
# Make the entire application directory writable by all users.
chmod -R 777 /usr/local/lib/$PACKAGE_NAME/ || true
exit 0
EOF

# 10. Make the postinst script executable
echo "--- Making postinst executable ---"
chmod +x "$BUILD_DIR/DEBIAN/postinst"

# 11. Build the Debian package
echo "--- Building Debian package ---"
dpkg-deb --build --root-owner-group "$BUILD_DIR"

# Rename the package to a more standard format
mv "${BUILD_DIR}.deb" "${PACKAGE_NAME}_${VERSION}_all.deb"

echo "--- Cleaning up build directory ---"
rm -rf "$BUILD_DIR"

echo "--- Build complete! Package created: ${PACKAGE_NAME}_${VERSION}_all.deb ---" 