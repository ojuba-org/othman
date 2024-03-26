# Maintainer: Mohamed Abdelhamed <secmohamed@protonmail.com>
pkgname=othman
pkgver=1.0.1
pkgrel=1
pkgdesc="Othman Quran Browser"
url="https://github.com/0x7cc/othman"
license=('Waqf Public License')
arch=('i686' 'x86_64')
makedepends=('meson' 'ninja')
source=("$pkgname-$pkgver.tar.gz::https://github.com/0x7cc/othman/archive/$pkgver.tar.gz")
sha256sums=('SKIP')

build() {
    cd "$pkgname-$pkgver"
    meson setup build --prefix /usr
    ninja -C build
}

check() {
    cd "$pkgname-$pkgver"
    meson test -C build
}

package() {
    cd "$pkgname-$pkgver"
    DESTDIR="$pkgdir" ninja -C build install
}
