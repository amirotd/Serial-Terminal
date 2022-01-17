#ifndef SERIALWIN_H
#define SERIALWIN_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class SerialWin; }
QT_END_NAMESPACE

class SerialWin : public QMainWindow
{
    Q_OBJECT

public:
    SerialWin(QWidget *parent = nullptr);
    ~SerialWin();

private slots:
    void on_openButton_clicked();

    void on_sendButton_clicked();

    void on_clearButton_clicked();

    void on_infoButton_clicked();

    void serialRecieved();

    void config_port();

    void on_closeButton_clicked();

    void on_refreshButton_clicked();

private:
    Ui::SerialWin *ui;
};
#endif // SERIALWIN_H
