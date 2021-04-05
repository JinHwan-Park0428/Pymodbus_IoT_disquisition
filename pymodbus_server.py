# --------------------------------------------------------------------------- # 
# 코드 동작에 필요한 import문을 추가
# --------------------------------------------------------------------------- #
from __future__ import print_function
from pymodbus.server.sync import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSparseDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import csv
import logging
# --------------------------------------------------------------------------- # 
# WARNING 이상의 Log를 출력
# --------------------------------------------------------------------------- #
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.WARNING)
# --------------------------------------------------------------------------- # 
# 클라이언트에서 넘어온 변환된 데이터를 전처리 과정을 통해 실제 값으로 변환 후
# 출력하고 CSV 파일로 저장 
# --------------------------------------------------------------------------- # 
class CustomDataBlock(ModbusSparseDataBlock):
    
    def setValues(self, address, value):
        # ------------------------------------------------------------------- # 
        # 들어온 데이터 갯수 만큼 반복하는 재귀함수
        # ------------------------------------------------------------------- # 
        super(CustomDataBlock, self).setValues(address, value)
        # ------------------------------------------------------------------- # 
        # 변환되어 들어온 데이터를 출력, 어떤 클라이언트로 재전송 하는지 주소 출력
        # 또한, 변환되어 들어온 데이터를 원래 보냈던 실제 값으로 변환 후 출력
        # ------------------------------------------------------------------- # 
        print("데이터 : {}, {}번 클라이언트로 응답".format(value, address))
        for a in range(0, 5) :
            if value[a] > 32767 and value[a] < 65536 :
                value[a] = value[a] - 65536
        print("실제 데이터 값 : {}".format(value))
        # ------------------------------------------------------------------- # 
        # 변환 한 실제 값을 csv 파일로 저장
        # ------------------------------------------------------------------- # 
        f = open('test.csv', 'a', encoding='utf-8', newline='')
        wr=csv.writer(f)
        wr.writerow(value)
        f.close()
# --------------------------------------------------------------------------- # 
# 클라이언트에서 전송한 데이터를 처리하기 위해, 데이터블럭, 저장소, 서버 정보 등을
# 설정하는 함수
# --------------------------------------------------------------------------- #
def run_custom_db_server():
    # ----------------------------------------------------------------------- # 
    # 데이터 블럭, 저장소, 컨텍스트등을 설정 하는 단계
    # ----------------------------------------------------------------------- #
    block  = CustomDataBlock([0]*100)
    store  = ModbusSlaveContext(hr=block, ir=block)
    context = ModbusServerContext(slaves=store, single=True)
    # ----------------------------------------------------------------------- # 
    # 서버 정보를 커스터마이징 하는 단계
    # ----------------------------------------------------------------------- #
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/bashwork/pymodbus/'
    identity.ProductName = 'pymodbus Server'
    identity.ModelName = 'pymodbus Server'
    identity.MajorMinorRevision = '2.4.0'
    # ----------------------------------------------------------------------- # 
    # 본인이 설정한 각종 정보를 토대로 TcpServer를 구현
    # address는 기본적으로 IP = "localhost", Port = 5020 으로 설정 되어있음 
    # ----------------------------------------------------------------------- #
    StartTcpServer(context, identity=identity, address=("localhost", 5020))
# --------------------------------------------------------------------------- # 
# 파이썬 코드가 main으로 실행될 경우에만 작
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    run_custom_db_server()