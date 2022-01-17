#include "serialwin.h"
#include "ui_serialwin.h"
#include <QSerialPort>
#include <QSerialPortInfo>
#include <QtSerialPort>
#include <QString>
#include <map>
#include <QTextEdit>
#include <QMessageBox>


typedef std::map<QString, qint32> baud_dict;
typedef std::map<QString, QSerialPort::DataBits> data_dict;
typedef std::map<QString, QSerialPort::Parity> parity_dict;
typedef std::map<QString, QSerialPort::StopBits> stop_dict;
typedef std::map<QString, QSerialPort::FlowControl> flow_dict;

QSerialPort *serial;

SerialWin::SerialWin(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::SerialWin)
{
    ui->setupUi(this);

    ui->closeButton->setEnabled(false);

//    const auto infos = QSerialPortInfo::availablePorts();
//    for(const QSerialPortInfo &info : infos)
//        ui->nameCombo->addItem(info.portName());

    QStringList baud_list = (QStringList()<<"1200"<<"2400"<<"4800"<<"9600"<<"19200"<<"38400"<<"57600"<<"115200");
    ui->baudCombo->addItems(baud_list);
    ui->baudCombo->setCurrentIndex(3);

    QStringList data_list = (QStringList()<<"5"<<"6"<<"7"<<"8");
    ui->dataCombo->addItems(data_list);
    ui->dataCombo->setCurrentIndex(3);

    QStringList parity_list = (QStringList()<<"NoParity"<<"EvenParity"<<"OddParity"<<"SpaceParity"<<"MarkParity");
    ui->parityCombo->addItems(parity_list);
    ui->parityCombo->setCurrentIndex(0);

    QStringList stop_list = (QStringList()<<"1"<<"1.5"<<"2");
    ui->stopCombo->addItems(stop_list);
    ui->stopCombo->setCurrentIndex(0);

    QStringList flow_list = (QStringList()<<"NoFlowControl"<<"HardwareControl"<<"SoftwareControl");
    ui->flowCombo->addItems(flow_list);
    ui->flowCombo->setCurrentIndex(0);

    config_port();
}

SerialWin::~SerialWin()
{
    delete ui;
    serial->close();
}


void SerialWin::on_openButton_clicked()
{
    if(ui->nameCombo->currentText().isEmpty()){
        QMessageBox::warning(this, "warning", "No port name specified");
    }
    else{
        serial->open(QIODevice::ReadWrite);
        connect(serial, SIGNAL(readyRead()), this, SLOT(serialRecieved()));
        ui->openButton->setEnabled(false);
        ui->closeButton->setEnabled(true);
    }
}


void SerialWin::on_sendButton_clicked()
{
    if(serial->isOpen()){
    QString send_text = ui->sendtext->toPlainText();
    QByteArray inBytes;
    const char *cStrData;
    inBytes = send_text.toUtf8();
    cStrData = inBytes.constData();
    QString qstrData;
    qstrData = QString::fromUtf8(cStrData);
    serial->write(cStrData);
    }
    else{
        QMessageBox::warning(this, "warning", "first open a port!");
    }
}


void SerialWin::on_clearButton_clicked()
{
    ui->recievetext->clear();
    ui->sendtext->clear();
}


void SerialWin::on_infoButton_clicked()
{
    QMessageBox::about(this, "about", "This is just a simple serial terminal!!");
}

void SerialWin::serialRecieved(){
    QString recieved_text = serial->readAll();
    if(recieved_text.length()>0){
        ui->recievetext->append(recieved_text);
    }
}


void SerialWin::config_port(){
    ui->nameCombo->clear();

    const auto infos = QSerialPortInfo::availablePorts();
    for(const QSerialPortInfo &info : infos)
        ui->nameCombo->addItem(info.portName());

    baud_dict m_baud;
    m_baud["1200"] = QSerialPort::Baud1200;
    m_baud["2400"] = QSerialPort::Baud2400;
    m_baud["4800"] = QSerialPort::Baud4800;
    m_baud["9600"] = QSerialPort::Baud9600;
    m_baud["19200"] = QSerialPort::Baud19200;
    m_baud["38400"] = QSerialPort::Baud38400;
    m_baud["57600"] = QSerialPort::Baud57600;
    m_baud["115200"] = QSerialPort::Baud115200;

    data_dict m_data;
    m_data["5"] = QSerialPort::Data5;
    m_data["6"] = QSerialPort::Data6;
    m_data["7"] = QSerialPort::Data7;
    m_data["8"] = QSerialPort::Data8;

    parity_dict m_parity;
    m_parity["NoParity"] = QSerialPort::NoParity;
    m_parity["EvenParity"] = QSerialPort::EvenParity;
    m_parity["OddParity"] = QSerialPort::OddParity;
    m_parity["SpaceParity"] = QSerialPort::SpaceParity;
    m_parity["MarkParity"] = QSerialPort::MarkParity;

    stop_dict m_stop;
    m_stop["1"] = QSerialPort::OneStop;
    m_stop["1.5"] = QSerialPort::OneAndHalfStop;
    m_stop["2"] = QSerialPort::TwoStop;

    flow_dict m_flow;
    m_flow["NoFlowControl"] = QSerialPort::NoFlowControl;
    m_flow["HardwareControl"] = QSerialPort::HardwareControl;
    m_flow["SoftwareControl"] = QSerialPort::SoftwareControl;

    serial = new QSerialPort(this);
    serial->setPortName(ui->nameCombo->currentText());
    serial->setBaudRate(m_baud[ui->baudCombo->currentText()]);
    serial->setDataBits(m_data[ui->dataCombo->currentText()]);
    serial->setParity(m_parity[ui->parityCombo->currentText()]);
    serial->setStopBits(m_stop[ui->stopCombo->currentText()]);
    serial->setFlowControl(m_flow[ui->flowCombo->currentText()]);
}


void SerialWin::on_closeButton_clicked()
{
    if(serial->isOpen()){
        serial->close();
        ui->openButton->setEnabled(true);
        ui->closeButton->setEnabled(false);
    }
}


void SerialWin::on_refreshButton_clicked()
{
    if(serial->isOpen()){
        serial->close();
        ui->openButton->setEnabled(true);
        ui->closeButton->setEnabled(false);
    }
    config_port();
}
