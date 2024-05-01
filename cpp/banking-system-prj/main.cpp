#include <iostream>
#include <memory>
#include <string>
#include <vector>

using namespace std;

class Acct {
   private:
    float amnt;

   public:
    Acct(float m_amnt) {
        cout << "hi" << endl;
        amnt = m_amnt;
    }

    float Amnt() {
        return amnt;
    }
};
class Bank {
    vector<Acct> accts;

   public:
    // Bank() { }

    bool create_acct(float initial) {
        cout << "create" << endl;
        accts.push_back(Acct(initial));
        return false;
    }
    bool deposit() {
        cout << "deposit" << endl;
        return false;
    }
    bool withdraw() {
        cout << "withdrawl" << endl;
        return false;
    }
    bool close_acct() {
        cout << "close" << endl;
        return false;
    }
    bool get_balance() {
        cout << "balance" << endl;
        return false;
    }
};

int main(int argc, char* argv[]) {
    cout << "Welcome to the bank" << endl
         << "\t(1) Create account" << endl
         << "\t(2) Deposit" << endl
         << "\t(3) Withdraw" << endl
         << "\t(4) Close the account" << endl
         << "\t(5) Balance enquiry" << endl
         << "\t(0) Exit" << endl;

    std::unique_ptr<Bank> bank = std::make_unique<Bank>();
    // std::unique_ptr<Bank> bank(new Bank());

    string s;
    if (argc > 1) {
        s = argv[1];
    }
    while (s != "0") {
        if (s == "1") {
            bank->create_acct(100);
        } else if (s == "2") {
            bank->deposit();
        } else if (s == "3") {
            bank->withdraw();
        } else if (s == "4") {
            bank->close_acct();
        } else if (s == "5") {
            bank->get_balance();
        }
        cout << "-> ";
        cin >> s;
    }
}
