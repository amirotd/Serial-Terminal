#include "serialwin.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    SerialWin w;
    w.show();
    return a.exec();
}
