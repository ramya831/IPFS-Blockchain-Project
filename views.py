from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate,  logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .blockchain import contract, w3
from .models import UserProfile
from .models import SharedData as SharedDataModel


import ipfshttpclient





# ======================
# LOGIN VIEW
# ======================
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'app/login.html', {'error': 'Invalid credentials'})

    return render(request, 'app/login.html')


#user register

def user_register(request):
    if request.method == "POST":
        full_name = request.POST['full_name']
        username = request.POST['username']
        email = request.POST['email']
        contact = request.POST['contact']
        address = request.POST['address']
        gender = request.POST['gender']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'app/user_register.html', {
                'error': 'Username already exists!'
            })

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        UserProfile.objects.create(
            user=user,
            full_name=full_name,
            email=email,
            contact=contact,
            address=address,
            gender=gender
        )

        return redirect('login')

    return render(request, 'app/user_register.html')


# ADMIN REGISTER
def admin_register(request):
    message = ""
    error = ""

    if request.method == "POST":
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            error = "Passwords do not match"
        elif User.objects.filter(username=username).exists():
            error = "Username already exists"
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=full_name
            )

            user.is_staff = True
            user.save()
            
            messages.success(request, "Admin registered successfully!")
            return redirect('login')

    return render(request, 'app/admin_register.html', {
        'message': message,
        'error': error
    })

        





# ======================
# HOME / DASHBOARD
# ======================
@login_required(login_url='login')
def home(request):
    return render(request, 'app/home.html')


# ======================
# UPLOAD FILE TO IPFS
# ======================
@login_required(login_url='login')
def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']

        client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
        result = client.add(uploaded_file)

        request.session['ipfs_hash'] = result['Hash']
        return redirect('share')
    
    return render(request, "app/upload.html", {
        'ipfs_hash': request.session.get('ipfs_hash')
    })


# ======================
# SHARE DATA (BLOCKCHAIN)
# ======================
@login_required(login_url='login')
def SharedData(request):
    ipfs_hash = request.session.get('ipfs_hash')

    if request.method == "POST":
        try:
            receiver = request.POST.get("receiver")
            file_hash = request.POST.get("file_hash")

            sender = w3.eth.accounts[0]

            tx_hash = contract.functions.shared_data(
                receiver,
                file_hash
            ).transact({"from": sender})

            w3.eth.wait_for_transaction_receipt(tx_hash)

            # ✅ SAVE TO DATABASE
            SharedData.objects.create(
                shared_user=request.user,
                file_hash=file_hash,
                receiver=receiver
            )

            return render(request, "app/SharedData.html", {
                "message": "Data shared successfully on blockchain ✅"
            })

        except Exception as e:
            return render(request, "app/SharedData.html", {
                "error": str(e)
            
            })# stay on same page

    users = User.objects.all()

    return render(request, "app/SharedData.html", {"users": users})
        

         

    
    
    





# ======================
# VIEW SHARED DATA
# ======================
@login_required(login_url='login')
def view_shared_messages(request):
    data = SharedDataModel.objects.filter(shared_user=request.user)
    return render(request, 'app/view_shared_messages.html', {'data': data})


# ======================
# GRAPH PAGE
# ======================
@login_required(login_url='login')
def graph(request):
    return render(request, 'app/graph.html')



# ======================
# LOGOUT
# ======================
@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')

def admin_logout(request):
    logout(request)
    return render(request, 'admin_logout.html')










@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)

    return render(request, "dashboard.html", {
        "role": profile.role
    })
    

    
    





